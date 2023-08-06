import random
import pandas as pd
import numpy as np
from .utils import (
    gcd,
    p_header,
    p_success,
    p_warning,
    p_fail,
)
from tqdm import tqdm

class EnKF:
    def __init__(self, prior, proxydb, seed=0, nens=100, recon_vars=['tas']):
        self.prior = prior
        self.pdb_assim = proxydb.filter(by='tag', keys=['assim'])
        self.pdb_eval = proxydb.filter(by='tag', keys=['eval'])
        self.seed = seed
        self.nens = nens
        self.recon_vars = recon_vars

    def gen_Ye(self):
        vn = list(self.prior.keys())[0]
        time = self.prior[vn].time
        random.seed(self.seed)
        sample_idx = random.sample(list(range(np.size(time))), self.nens)
        self.prior_sample_idx = sample_idx
        self.prior_sample_years = time[sample_idx]

        self.Ye = {}
        self.Ye_df = {}
        self.Ye_lat = {}
        self.Ye_lon = {}
        self.Ye_coords = {}
        for tag in ['assim', 'eval']:
            target_pdb = self.__dict__[f'pdb_{tag}']
            self.Ye_df[tag] = pd.DataFrame(index=time)
            self.Ye_lat[tag] = []
            self.Ye_lon[tag] = []
            self.Ye_coords[tag] = np.ndarray((target_pdb.nrec, 2))

            series_dict = {}
            for pid, pobj in target_pdb.records.items():
                series = pd.Series(index=pobj.pseudo.time, data=pobj.pseudo.value)
                series_dict[pid] = series
                self.Ye_lat[tag].append(pobj.lat)
                self.Ye_lon[tag].append(pobj.lon)

            if len(series_dict) > 0:
                self.Ye_df[tag] = pd.concat(series_dict, axis=1)
            else:
                self.Ye_df[tag] = pd.DataFrame()

            self.Ye_df[tag].dropna(inplace=True)
            self.Ye[tag] = np.array(self.Ye_df[tag])[sample_idx].T

            self.Ye_coords[tag][:, 0] = self.Ye_lat[tag]
            self.Ye_coords[tag][:, 1] = self.Ye_lon[tag]
        

    def gen_Xb(self):
        vn_1st = list(self.prior.keys())[0]
        Xb_var_irow = {}  # index of rows in Xb to store the specific var
        loc = 0
        for vn in self.recon_vars:
            nt, nlat, nlon = np.shape(self.prior[vn].da.values)
            lats, lons = self.prior[vn].da.lat.values, self.prior[vn].da.lon.values
            lon2d, lat2d = np.meshgrid(lons, lats)
            fd_coords = np.ndarray((nlat*nlon, 2))
            fd_coords[:, 0] = lat2d.flatten()
            fd_coords[:, 1] = lon2d.flatten()
            fd = self.prior[vn].da.values[self.prior_sample_idx]
            fd = np.moveaxis(fd, 0, -1)
            fd_flat = fd.reshape((nlat*nlon, self.nens))
            if vn == vn_1st:
                Xb = fd_flat
                Xb_coords = fd_coords
            else:
                Xb = np.concatenate((Xb, fd_flat), axis=0)
                Xb_coords = np.concatenate((Xb_coords, fd_coords), axis=0)
            Xb_var_irow[vn] = [loc, loc+nlat*nlon-1]
            loc += nlat*nlon

        self.Xb = Xb
        self.Xb_coords = Xb_coords
        self.Xb_var_irow = Xb_var_irow
        self.Xb_aug = np.append(self.Xb, self.Ye['assim'], axis=0)
        self.Xb_aug = np.append(self.Xb_aug, self.Ye['eval'], axis=0)
        self.Xb_aug_coords = np.append(self.Xb_coords, self.Ye_coords['assim'], axis=0)
        self.Xb_aug_coords = np.append(self.Xb_aug_coords, self.Ye_coords['eval'], axis=0)

    def update_yr(self, target_yr, recon_loc_rad=25000, recon_timescale=1, debug=False):
        start_yr = target_yr - recon_timescale/2
        end_yr = target_yr + recon_timescale/2
        Xb = np.copy(self.Xb_aug)

        i = 0
        for pid, pobj in self.pdb_assim.records.items():
            mask = (pobj.time >= start_yr) & (pobj.time <= end_yr)
            nYobs = np.sum(mask)
            if nYobs == 0:
                i += 1
                continue  # skip to next proxy record
            
            Yobs = pobj.value[mask].mean()
            loc = cov_localization(recon_loc_rad, pobj, self.Xb_aug_coords)
            Ye = Xb[i - (self.pdb_assim.nrec+self.pdb_eval.nrec)]
            ob_err = pobj.R / nYobs
            Xa = enkf_update_array(Xb, Yobs, Ye, ob_err, loc=loc, debug=debug)

            if debug:
                Xb_mean = Xb[:-(self.pdb_assim.nrec+self.pdb_eval.nrec)].mean()
                Xa_mean = Xa[:-(self.pdb_assim.nrec+self.pdb_eval.nrec)].mean()
                innov = Yobs - Ye.mean()
                if np.abs(innov / Yobs) > 1:
                    print(pid, i - (self.pdb_assim.nrec+self.pdb_eval.nrec))
                    print(f'\tXb_mean: {Xb_mean:.2f}, Xa_mean: {Xa_mean:.2f}')
                    print(f'\tInnovation: {innov:.2f}, ob_err: {ob_err:.2f}, Yobs: {Yobs:.2f}, Ye_mean: {Ye.mean():.2f}')

            Xbvar = Xb.var(axis=1, ddof=1)
            Xavar = Xa.var(axis=1, ddof=1)
            vardiff = Xavar - Xbvar
            if (not np.isfinite(np.min(vardiff))) or (not np.isfinite(np.max(vardiff))):
                raise ValueError('Reconstruction has blown-up. Exiting!')

            if debug: print('min/max change in variance: ('+str(np.min(vardiff))+','+str(np.max(vardiff))+')')
            i += 1

            Xb = Xa

        return Xb

    def run(self, recon_yrs=np.arange(1, 2001), recon_loc_rad=25000, recon_timescale=1, verbose=False, debug=False):
        self.gen_Ye()
        self.gen_Xb()

        nt = np.size(recon_yrs)
        nrow, nens = np.shape(self.Xb_aug)

        self.Xa = np.ndarray((nt, nrow, nens))


        for yr_idx, target_yr in enumerate(tqdm(recon_yrs, desc='KF updating')):
            self.Xa[yr_idx] = self.update_yr(target_yr, recon_loc_rad, recon_timescale, debug=debug)

        self.recon_fields = {}
        for vn, irow in self.Xb_var_irow.items():
            _, nlat, nlon = np.shape(self.prior[vn].da.values)
            self.recon_fields[vn] = self.Xa[:, irow[0]:irow[-1]+1, :].reshape((nt, nlat, nlon, nens))
            self.recon_fields[vn] = np.moveaxis(self.recon_fields[vn], -1, 1)

        if verbose: p_success(f'>>> EnKF.recon_fields created')
    

def enkf_update_array(Xb, obvalue, Ye, ob_err, loc=None, debug=False):
    """ Function to do the ensemble square-root filter (EnSRF) update

    (ref: Whitaker and Hamill, Mon. Wea. Rev., 2002)

    Originator:
        G. J. Hakim, with code borrowed from L. Madaus Dept. Atmos. Sciences, Univ. of Washington

    Revisions:
        1 September 2017: changed varye = np.var(Ye) to varye = np.var(Ye,ddof=1) for an unbiased calculation of the variance. (G. Hakim - U. Washington)

    Args:
        Xb: background ensemble estimates of state (Nx x Nens)
        obvalue: proxy value
        Ye: background ensemble estimate of the proxy (Nens x 1)
        ob_err: proxy error variance
        loc: localization vector (Nx x 1) [optional]
        inflate: scalar inflation factor [optional]
    """

    # Get ensemble size from passed array: Xb has dims [state vect.,ens. members]
    Nens = Xb.shape[1]

    # ensemble mean background and perturbations
    xbm = np.mean(Xb,axis=1)
    Xbp = np.subtract(Xb,xbm[:,None])  # "None" means replicate in this dimension

    # ensemble mean and variance of the background estimate of the proxy
    mye   = np.mean(Ye)
    varye = np.var(Ye,ddof=1)

    # lowercase ye has ensemble-mean removed
    ye = np.subtract(Ye, mye)

    # innovation
    try:
        innov = obvalue - mye
    except:
        print('innovation error. obvalue = ' + str(obvalue) + ' mye = ' + str(mye))
        print('returning Xb unchanged...')
        return Xb

    # innovation variance (denominator of serial Kalman gain)
    kdenom = (varye + ob_err)

    # numerator of serial Kalman gain (cov(x,Hx))
    kcov = np.dot(Xbp,np.transpose(ye)) / (Nens-1)

    # Option to inflate the covariances by a certain factor
    #if inflate is not None:
    #    kcov = inflate * kcov # This implementation is not correct. To be revised later.

    # Option to localize the gain
    if loc is not None:
        kcov = np.multiply(kcov,loc)

    # Kalman gain
    kmat = np.divide(kcov, kdenom)

    # update ensemble mean
    xam = xbm + np.multiply(kmat,innov)

    # update the ensemble members using the square-root approach
    beta = 1./(1. + np.sqrt(ob_err/(varye+ob_err)))
    kmat = np.multiply(beta,kmat)
    ye   = np.array(ye)[np.newaxis]
    kmat = np.array(kmat)[np.newaxis]
    Xap  = Xbp - np.dot(kmat.T, ye)

    # full state
    Xa = np.add(xam[:,None], Xap)

    # if masked array, making sure that fill_value = nan in the new array
    if np.ma.isMaskedArray(Xa): np.ma.set_fill_value(Xa, np.nan)

    # Return the full state
    return Xa

def cov_localization(locRad, Y, X_coords):
    """ Originator: R. Tardif, Dept. Atmos. Sciences, Univ. of Washington
    -----------------------------------------------------------------
     Inputs:
        locRad : Localization radius (distance in km beyond which cov are forced to zero)
             Y : Proxy object, needed to get ob site lat/lon (to calculate distances w.r.t. grid pts
      X_coords : Array containing geographic location information of state vector elements

     Output:
        covLoc : Localization vector (weights) applied to ensemble covariance estimates.
                 Dims = (Nx x 1), with Nx the dimension of the state vector.

     Note: Uses the Gaspari-Cohn localization function.

    """

    # declare the localization array, filled with ones to start with (as in no localization)
    stateVectDim, nbdimcoord = X_coords.shape
    covLoc = np.ones(shape=[stateVectDim],dtype=np.float64)

    # Mask to identify elements of state vector that are "localizeable"
    # i.e. fields with (lat,lon)
    localizeable = covLoc == 1. # Initialize as True

    # array of distances between state vector elements & proxy site
    # initialized as zeros: this is important!
    dists = np.zeros(shape=[stateVectDim])

    # geographic location of proxy site
    site_lat = Y.lat
    site_lon = Y.lon
    # geographic locations of elements of state vector
    X_lon = X_coords[:,1]
    X_lat = X_coords[:,0]

    # calculate distances for elements tagged as "localizeable".
    dists[localizeable] = np.array(
        gcd(site_lon, site_lat, X_lon[localizeable], X_lat[localizeable]),
        dtype=np.float64,
    )

    # those not "localizeable" are assigned with a disdtance of "nan"
    # so these elements will not be included in the indexing
    # according to distances (see below)
    dists[~localizeable] = np.nan

    # Some transformation to variables used in calculating localization weights
    hlr = 0.5*locRad; # work with half the localization radius
    r = dists/hlr

    # indexing w.r.t. distances
    ind_inner = np.where(dists <= hlr)    # closest
    ind_outer = np.where(dists >  hlr)    # close
    ind_out   = np.where(dists >  2.*hlr) # out

    # Gaspari-Cohn function
    # for pts within 1/2 of localization radius
    covLoc[ind_inner] = (((-0.25*r[ind_inner]+0.5)*r[ind_inner]+0.625)* \
                         r[ind_inner]-(5.0/3.0))*(r[ind_inner]**2)+1.0
    # for pts between 1/2 and one localization radius
    covLoc[ind_outer] = ((((r[ind_outer]/12. - 0.5) * r[ind_outer] + 0.625) * \
                          r[ind_outer] + 5.0/3.0) * r[ind_outer] - 5.0) * \
                          r[ind_outer] + 4.0 - 2.0/(3.0*r[ind_outer])
    # Impose zero for pts outside of localization radius
    covLoc[ind_out] = 0.0

    # prevent negative values: calc. above may produce tiny negative
    # values for distances very near the localization radius
    # TODO: revisit calculations to minimize round-off errors
    covLoc[covLoc < 0.0] = 0.0

    return covLoc

