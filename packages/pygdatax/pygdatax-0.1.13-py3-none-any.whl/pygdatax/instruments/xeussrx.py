import numpy as np
from pygdatax import nxlib
from pygdatax import flib
import nexusformat.nexus as nx
from scipy import ndimage
from scipy.special import erf
from lmfit.model import Model, fit_report

@nxlib.rxtreatment_function
def set_roi(root: nx.NXroot, roi_width: int = 20, roi_height: int = 10) -> None:
    """
    Set roi width and height with the raw_data/direct_beam field
    Args:
        root: NXroot
        roi_width:
        roi_height:

    Returns:

    """
    if roi_width:
        root.raw_data.direct_beam.roi_width = roi_width
    if roi_height:
        root.raw_data.direct_beam.roi_height = roi_height


@nxlib.rxtreatment_function
def set_center(root: nx.NXroot, x0: float = None, y0: float = None) -> None:
    """
    Set beam center position within the raw_data/direct_beam field
    Args:
        root: NXroot
        x0: horizontal beam center position
        y0: vertical beam center

    Returns:

    """
    if x0:
        root.raw_data.direct_beam.x0 = x0
    if y0:
        root.raw_data.direct_beam.y0 = y0


@nxlib.rxtreatment_function
def set_distance(root: nx.NXroot, distance: float = None) -> None:
    """
    Set sample to detector distance in mm
    Args:
        root: NXroot
        distance: sample to detector distance in mm

    Returns:

    """
    root.raw_data.instrument.detector.distance = distance


@nxlib.rxtreatment_function
def set_offset(root: nx.NXroot, offset: float = None) -> None:
    """
    Set sample offset within the raw_data/sample/offset field
    Args:
        root: NXroot
        offset: sample angular offset in degree

    Returns:

    """
    if offset is not None:
        root.raw_data.sample.offset = offset


@nxlib.rxtreatment_function
def find_center(root, roi=None):
    if roi is None:
        x0 = root.raw_data.direct_beam.x0.nxdata
        y0 = root.raw_data.direct_beam.y0.nxdata
        w = root.raw_data.direct_beam.roi_width.nxdata
        h = root.raw_data.direct_beam.roi_height.nxdata
        roi = flib.get_roi(x0, y0, w, h)
    cropM = flib.crop_image(root.raw_data.direct_beam.data.data.nxdata, roi)
    centerCrop = ndimage.measurements.center_of_mass(cropM, index='int')
    center = [centerCrop[1] + roi[0], centerCrop[0] + roi[1]]
    root.raw_data.direct_beam.x0 = center[0]
    root.raw_data.direct_beam.y0 = center[1]
    print('x0 = %.3f \n y0= %.3f' % (center[0], center[1]))


@nxlib.rxtreatment_function
def set_distance(root, distance=None):
    if distance:
        root.raw_data.instrument.detector.distance = distance


@nxlib.rxtreatment_function
def compute_ref(root):
    omega = root.raw_data.sample.om.nxdata
    count_time = root.raw_data.sample.count_time.nxdata
    theta = omega-root.raw_data.sample.offset.nxdata
    wavelength = root.raw_data.instrument.source.incident_wavelength.nxdata
    nPoints = len(theta)
    q = 4*np.pi/wavelength*np.sin(theta*np.pi/180)
    r = np.zeros(nPoints)
    dr = np.zeros(nPoints)
    count = np.zeros(nPoints)
    specPosX = np.zeros(nPoints)
    specPosY = np.zeros(nPoints)
    distance = root.raw_data.instrument.detector.distance.nxdata
    x0 = root.raw_data.direct_beam.x0.nxdata
    y0 = root.raw_data.direct_beam.y0.nxdata
    roi_width = root.raw_data.direct_beam.roi_width.nxdata
    roi_height = root.raw_data.direct_beam.roi_height.nxdata
    # d = root.raw_data.image_stack.data.nxdata
    sumEB = flib.sumSpec(root.raw_data.direct_beam.data.data.nxdata, 0, distance, x0, y0,
                         roi_width, roi_height, pixelSize=0.172)
    sumEB /= root.raw_data.direct_beam.count_time.nxdata
    root.raw_data.direct_beam.flux = nx.NXfield(sumEB, attrs={'units': r's$^{-1}$'})
    # with root.raw_data.image_stack.data as slab:
    #     ni, nj, nk = slab.nxdims
    #     size = [1, 1, Nk]
    #     for i in range(Ni):
    #         for j in range(Nj):
    #             value = slab.nxget([i, j, 0], size)
    # Ni, Nj, Nk = slab.nxdims
    # size = [1, 1, Nk]
    # for i in range(Ni):
    #     for j in range(Nj):
    #         value = slab.nxget([i, j, 0], size)
    for i in range(nPoints):
        if flib.roi_is_on_gap(x0, y0, roi_width, roi_height, theta[i], distance):
            count[i] = np.nan
            specPosX[i] = np.nan
            specPosY[i] = np.nan
        else:
            d = root.raw_data.image_stack.data[i, :, :]
            count[i] = flib.sumSpec(d, theta[i], distance, x0, y0,
                                    roi_width, roi_height, pixelSize=0.172)
            # correction by solid angle
            count[i] /= np.cos(2*np.deg2rad(theta[i]))**3
            # find specular position
            specPosX[i], specPosY[i] = flib.getSpecularPostion(d, x0, y0, roi_width, roi_height, theta[i],
                                                               distance, pixelSize=0.172, extraHeight=60, extraWidth=60)

    ref = nx.NXentry()
    # specular data
    ref.data = nx.NXdata()
    r = count / sumEB / root.raw_data.sample.count_time.nxdata
    # removing nan
    # index = ~np.isnan(count)
    # q = q[index]
    # r = r[index]
    # specPosX = specPosX[index]
    # specPosY = specPosY[index]
    # count = count[index]
    # omega = omega[index]
    ref.data.nxsignal = nx.NXfield(r, name='R')
    ref.data.nxerrors = r / np.sqrt(count)
    ref.data.nxaxes = [nx.NXfield(q, name='Q', attrs={'units': r'$\AA^{-1}$'})]
    ref.attrs['default'] = 'data'
    # specular postion
    # remove nan
    index = ~np.isnan(r / np.sqrt(count))
    specular_position = nx.NXdata()
    specular_position.nxsignal = nx.NXfield(y0-specPosY[index], name='specPosY')
    # remove nan from specualr position

    specular_position.nxaxes = [nx.NXfield(omega[index], name='omega', attrs={'units': 'deg'})]
    specular_position.specPosX = nx.NXfield(x0-specPosX[index], name='specPosX')
    ref.specular_position = specular_position

    if 'reflectivity' in root.keys():
        del root['reflectivity']
    root.reflectivity = ref
    root.attrs['default'] = 'reflectivity'
    return


@nxlib.rxtreatment_function
def autoset_roi(root):
    m = root.raw_data.direct_beam.data.data.nxdata
    x0 = root.raw_data.direct_beam.x0.nxdata
    y0 = root.raw_data.direct_beam.y0.nxdata
    roi_width = root.raw_data.direct_beam.roi_width.nxdata
    roi_height = root.raw_data.direct_beam.roi_height.nxdata
    x1 = x0 - roi_width/2-30
    y1 = y0 - roi_height/2-30
    x2 = x0 + roi_width/2+30
    y2 = y0 + roi_height/2+30
    cropM = flib.crop_image(m, [x1, y1, x2, y2])
    y, x = np.indices(cropM.shape)

    def function(u, v, amplitude, sigx, sigy, u0, v0, bkg):
        val = amplitude * np.exp(-((u - u0) ** 2 / (2 * sigx ** 2) + (v - v0) ** 2 / (2 * sigy ** 2))) + bkg
        return val.flatten()

    model = Model(function, independent_vars=["u", "v"],
                  param_names=["amplitude", "sigx", "sigy", "u0",
                               "v0", "bkg"])
    params = model.make_params()
    params['bkg'].value = 0
    params['bkg'].vary = False
    params['amplitude'].value = np.max(cropM)
    params['sigy'].value = 2
    params['sigx'].value = 2
    params['u0'].value = roi_width/2
    params['v0'].value = roi_height/2
    result = model.fit(cropM.flatten(), u=x, v=y, params=params)
    print(result.fit_report())
    fitParams = result.params
    root.raw_data.direct_beam.roi_width = int(np.abs(15*fitParams['sigx'].value))
    root.raw_data.direct_beam.roi_height = int(np.abs(15*fitParams['sigy'].value))


@nxlib.rxtreatment_function
def off_specular_map(root: nx.NXroot) -> None:
    """
    compute the off specular data
    Args:
        root:

    Returns:

    """
    nPoints = len(root.raw_data.sample.om.nxdata)
    imageShape = root.raw_data.direct_beam.data.data.nxdata.shape
    offMap = np.empty((imageShape[0], nPoints))
    # stack = root.raw_data.image_stack.data.nxdata
    x0 = root.raw_data.direct_beam.x0.nxdata
    y0 = root.raw_data.direct_beam.y0.nxdata
    roi_width = root.raw_data.direct_beam.roi_width.nxdata
    distance = root.raw_data.instrument.detector.distance.nxdata
    alphai = root.raw_data.sample.om.nxdata - root.raw_data.sample.offset.nxdata
    alphaf = np.arctan((y0-np.arange(imageShape[0]))*0.172/distance)/2*180/np.pi
    roi = [x0-roi_width/2, 0, x0+roi_width/2, imageShape[0]]
    for i in range(nPoints):
        d = root.raw_data.image_stack.data[i, :, :]
        cropM = flib.crop_image(d.nxdata, roi)
        offMap[:, i] = np.sum(cropM, axis=1) / root.raw_data.sample.count_time.nxdata[i]
    # q = np.sin(np.deg2rad(alphai+alphaf))*4*np.pi/1.542
    offData = nx.NXdata()
    offData.nxsignal = nx.NXfield(offMap, name='data')
    offData.nxaxes = [nx.NXfield(alphaf, name='alpha_f', attrs={'units': 'deg'}),
                      nx.NXfield(alphai, name='alpha_i', attrs={'units': 'deg'})
                      ]
    offData.attrs['interpretation'] = "image"

    entry = nx.NXentry()
    entry.attrs['default'] = 'data'
    entry.data = offData
    if 'off_specular' in root.keys():
        del root['off_specular']
    root.off_specular = entry


@nxlib.rxtreatment_function
def remap_offspecular(root: nx.NXroot, qx_bins: int = 500, qz_bins: int = 500) -> None:
    """
    remap the angular off specualr map to qx, qz off specular map and store it with the off_specular entry
    Args:
        root: NXroot
        qx_bins: number of bins for qx
        qz_bins: number of bins for qz
    """
    if 'off_specular' not in root.keys():
        off_specular_map(root.file_name)
    wavelength = root.raw_data.instrument.source.incident_wavelength.nxdata
    data = root.off_specular.data.data.nxdata
    alphai = np.deg2rad(root.off_specular.data.alpha_i.nxdata)
    alphaf = np.deg2rad(root.off_specular.data.alpha_f.nxdata)
    alphaiGrid, alphafGrid = np.meshgrid(alphai, alphaf)
    qz = 2*np.pi / wavelength * (np.sin(alphaiGrid) + np.sin(alphafGrid))
    qx = 2*np.pi / wavelength * (np.cos(alphafGrid) - np.cos(alphaiGrid))
    count, b, c = np.histogram2d(qx.flatten(), qz.flatten(), (qx_bins, qz_bins))
    count1 = np.maximum(1, count)
    bins_qx = (b[1:] + b[:-1]) / 2.0
    bins_qz = (c[1:] + c[:-1]) / 2.0
    sum_, b, c = np.histogram2d(qx.flatten(), qz.flatten(), (qx_bins, qz_bins),
                                weights=data.flatten())
    i = sum_ / count1
    i[count == 0] = -1
    if 'data_Q' in root.off_specular:
        del root['off_specular/data_Q']
    root.off_specular.data_Q = nx.NXdata(signal=i, name='data',
                                         axes=(nx.NXfield(bins_qx, name='Qx'),
                                               nx.NXfield(bins_qz, name='Qz')))


@nxlib.rxtreatment_function
def footprint_correction(root, length=None, width=None, beam_profile='uniform'):
    if length is None:
        length = root.raw_data.sample.length.nxdata
    else:
        root.raw_data.sample.length = length
    if width is None:
        width = root.raw_data.instrument.slit.y_gap.nxdata
    else:
        root.raw_data.instrument.slit.y_gap = width
    if 'reflectivity' in root:
        theta = np.arcsin(root.reflectivity.data.Q.nxdata * root.raw_data.instrument.source.incident_wavelength.nxdata /
                          (4*np.pi))
        thetaf = np.arcsin(width/length)
        if beam_profile == 'uniform':
            fp = 1/np.sin(theta)*width/length
            fp[theta >= thetaf] = 1
        elif beam_profile =='gaussian':
            fp = 1/erf(np.sin(theta)*length/2/(2**0.5*width))
        r_corr = root.reflectivity.data.nxsignal.nxdata * fp
        r_corr_error = root.reflectivity.data.nxerrors.nxdata * fp
        data_corr = nx.NXdata(signal=nx.NXfield(r_corr, name='R_corr'),
                              axes=root.reflectivity.data.nxaxes,
                              errors=r_corr_error)
        if 'data_corr' in root.reflectivity:
            del root['reflectivity/data_corr']
        root.reflectivity.data_corr = data_corr
        root.reflectivity.attrs['default'] = "data_corr"


@nxlib.rxtreatment_function
def save_as_txt(root: nx.NXroot) -> None:
    """
    Save the reflecticity spectra within two text files. One corresponds to the non corrected data, the other to the footprint
    corrected data
    Args:
        root: NXroot

    Returns:

    """
    if 'reflectivity' in root:
        x = root.reflectivity.data.nxaxes[0].nxdata
        y = root.reflectivity.data.nxsignal.nxdata
        dy = root.reflectivity.data.nxerrors.nxdata
        # remove nan
        index = ~np.isnan(dy)
        mat = np.stack((x[index], y[index], dy[index]))
        newfile = root.file_name.split('.')[0] + '.txt'
        header = 'Q \t R \t dR'
        np.savetxt(newfile, mat.transpose(), delimiter='\t', header=header)
        if 'data_corr' in root.reflectivity:
            x = root.reflectivity.data_corr.nxaxes[0].nxdata
            y = root.reflectivity.data_corr.nxsignal.nxdata
            dy = root.reflectivity.data_corr.nxerrors.nxdata
            # remove nan
            index = ~np.isnan(dy)
            mat = np.stack((x[index], y[index], dy[index]))
            newfile = root.file_name.split('.')[0] + '_corr' + '.txt'
            header = 'Q \t R_corrected \t dR_corrected '
            np.savetxt(newfile, mat.transpose(), delimiter='\t', header=header)


@nxlib.rxtreatment_function
def fit_distance_and_offset(root, fit_distance=True, fit_offset=True, om_range=[-np.inf, np.inf]):
    if 'reflectivity' not in root:
        return

    def fun(x, distance, offset):
        return np.tan(2*np.deg2rad(x-offset)) * distance / 0.172

    model = Model(fun)
    distanceIni = root.raw_data.instrument.detector.distance.nxdata
    offsetIni = root.raw_data.sample.offset.nxdata
    params = model.make_params(distance=distanceIni, offset=offsetIni)
    params['distance'].vary = fit_distance
    params['offset'].vary = fit_offset

    om = root.reflectivity.specular_position.omega.nxdata
    specPos = root.reflectivity.specular_position.specPosY.nxdata
    index = np.logical_and(om >= om_range[0], om <= om_range[1])

    res = model.fit(specPos[index], params, x=om[index])
    print(res.fit_report())
    # res.plot()
    root.raw_data.instrument.detector.distance = res.params['distance'].value
    root.raw_data.sample.offset = res.params['offset']


def automatic_treatment(data_folder, distance=1216):
    file = nxlib.build_rxnexus_from_directory(data_folder, distance=distance)
    find_center(file)
    autoset_roi(file)
    compute_ref(file)
    root = nx.nxload(file)
    offset = root.raw_data.sample.offset.nxdata
    root.close()
    fit_distance_and_offset(file, fit_distance=True, fit_offset=True, om_range=[offset+0.2, offset+1.5])
    compute_ref(file)



if __name__ == '__main__':
    import os
    ########################################################################################
    import matplotlib.pyplot as plt
    # folder = '/home/achennev/Bureau/PIL pour tiago/RX_tiago/9_11_2020/TH10_10_1_pos1'
    # # folder2 = '/home/achennev/Bureau/PIL pour tiago/RX_tiago/9_11_2020/TH10_10_1_pos2'
    # folder = '/home/achennev/Bureau/PIL pour tiago/RX_tiago/9_11_2020/wafer_nue_pos1'
    # folder2 = '/home/achennev/Bureau/PIL pour tiago/RX_tiago/9_11_2020/wafer_nue_pos2'
    #
    # file = os.path.join(folder, 'wafer_nue_pos1.nxs')
    #
    # set_distance(file, distance=1214)
    # set_offset(file, offset=-0.12)
    # find_center(file, roi=[460, 900, 600, 1000])
    # autoset_roi(file)
    #
    # # autoset_roi(file2)
    # # set_roi(file, roi_height=5)
    # # set_roi(file2, roi_width=60, roi_height=40)
    # compute_ref(file)
    # footprint_correction(file, width=0.269, length=26)
    # off_specular_map(file)
    # remap_offspecular(file, qx_bins=300, qz_bins=300)
    # save_as_txt(file)
    # # file2 = os.path.join(folder2, 'wafer_nue_pos2.nxs')
    # # set_distance(file2, distance=1212)
    # # set_offset(file2, offset=-0.137)
    # # find_center(file2, roi=[460, 960, 600, 1020])
    # #
    # # compute_ref(file2)
    # # footprint_correction(file2)
    ###########################################################################
    # folder = '/home/achennev/Bureau/PIL pour tiago/RX_tiago/9_11_2020/TH1_10_2000rpm_pos1'
    # folder = '/home/achennev/Documents/xeuss/Depot_Au_EchSOLEIL_pos2'
    # automatic_treatment(folder, distance=1214)
    file1 = '/home/achennev/Documents/xeuss/Depot_Au_EchSOLEIL_pos1.nxs'
    off_specular_map(file1)
