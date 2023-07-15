import numpy as np


# %% packSPH
def packSPH(siz=5, r=0.5, typ='HCP'):
    """
    PACKSPH returns the HCP or FCC packing of siz spheres of radius r

    Args:
    siz: array_like, [5, 5, 5] number of spheres along x,y,z
         if siz is a scalar, the same siz is applied to all dimensions [siz, siz, siz]
    r: float, bead radius
    typ: str, optional, 'HCP' (default, period 2) or 'FCC' (period 3)

    Returns:
    X: array_like, [size(1) x size(2) x size(3)] x 3 centers


    Example:

        import matplotlib.pyplot as plt
        from utils.SPHtools import packSPH

        X = packSPH(5)

        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(X[:, 0], X[:, 1], X[:, 2], s=10, c='b', alpha=0.5)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()

    """
    # 2023-02-20 | INRAE\Olivier Vitrac, Han Chen | rev. 2023-02-21

    # arg check
    rdefault = 0.5
    typdefault = 'HCP'
    sizedefault = 5

    if siz is None: siz = sizedefault
    if r is None: r = rdefault
    if typ == '':typ = typdefault
    if np.size(siz) == 1:siz = np.array([siz, siz, siz])
    if len(siz) != 3: raise ValueError('siz must be 1x3 or 3x1 vector')
    if not isinstance(typ, str):raise TypeError('typ must be a char array')

    # flag
    forceFCC = 0 if typ.upper() == 'HCP' else 1

    # Lattice
    i, j, k = np.mgrid[0:siz[0], 0:siz[1], 0:siz[2]]
    i, j, k = i.flatten(), j.flatten(), k.flatten()

    X = np.zeros((np.size(i), 3))
    X[:, 0] = 2 * i + np.mod(j + k, 2)
    X[:, 1] = np.sqrt(3) * (j + np.mod(k, 2) / 3) + (np.mod(k, 3) == 2) * forceFCC
    X[:, 2] = 2 * np.sqrt(6) * k / 3

    return r * X

# %% kernelSPH
def kernelSPH(h=None, typ='lucy', d=3):
    """
    KERNELSPH return a SPH kernel

    Syntax:
        W = kernelSPH(h,typ,d)
    Inputs:
            h : cutoff
          typ : kernel name (default = Lucy)
            d : dimension
    Output:
            W : kernel function lambda r: ...

    Example:
        from utils.SPHtools import kernelSPH
        W = kernelSPH(1,'lucy',3)

    See also: interp3SPH, interp2SPH, packSPH
    """
    # 2023-02-20 | INRAE\Olivier Vitrac, Han Chen | rev. 2023-02-21

    # arg check
    if h is None:
        raise ValueError('Supply a value for h')
    if typ is None:
        typ = 'lucy'
    if not isinstance(typ, str):
        raise ValueError('typ must be a string')
    if d is None:
        d = 3
    if d < 2 or d > 3:
        raise ValueError('d must be equal to 1, 2 or 3')

    # main
    if typ.lower() == 'lucy':

        if d == 3:
            # W = @(r) (r<h) .* (1.0./h.^3.*(r./h-1.0).^3.*((r.*3.0)./h+1.0).*(-1.05e+2./1.6e+1))./pi;
            W = lambda r, h=h: np.double(r < h) * \
            (1.0/h**3 * (r/h - 1.0)**3 * ((r*3.0)/h + 1.0) * (-1.05e+2/1.6e+1) / np.pi)
        elif d == 2:
            #  W = @(r) (r<h) .* (1.0./h.^2.*(r./h-1.0).^3.*((r.*3.0)./h+1.0).*-5.0)./pi;
            W = lambda r, h=h: np.double(r < h) * \
            (1.0/h**2 * (r/h - 1.0)**3 * ((r*3.0)/h + 1.0) * (-5.0) / np.pi)

    elif typ.lower() == 'lucyder':
        if d == 3:
            # W = @(r) (r<h) .* (1.0./h.^4.*(r./h-1.0).^3.*(-3.15e+2./1.6e+1))./pi-(1.0./h.^4.*(r./h-1.0).^2.*((r.*3.0)./h+1.0).*(3.15e+2./1.6e+1))./pi;
            W = lambda r,h=h: np.double(r < h) * \
                (\
                1.0/h**4 * (r/h - 1.0)**3 * (-3.15e+2/1.6e+1) / np.pi \
                - 1.0/h**4 * (r/h - 1.0)**2 * ((r*3.0)/h + 1.0) * (3.15e+2/1.6e+1) / np.pi \
                )
        elif d == 2:
            # W = @(r) (r<h) .* (1.0./h.^3.*(r./h-1.0).^3.*-1.5e+1)./pi-(1.0./h.^3.*(r./h-1.0).^2.*((r.*3.0)./h+1.0).*1.5e+1)./pi;
            W = lambda r,h=h: np.double(r < h) * \
                ( \
                1.0/h**3 * (r/h - 1.0)**3 * (-1.5e+1) / np.pi
                - 1.0/h**3 * (r/h - 1.0)**2 * ((r*3.0)/h + 1.0) * (1.5e+1) / np.pi \
                )
        else:
            raise NotImplementedError(f"the kernel '{typ}' is not implemented")

    return W


# %%interp3SPH

def interp3SPH(centers = packSPH(5),
               y = np.array([]),
               Xq =None,
               Yq =None,
               Zq =None,
               W = kernelSPH(1,'lucy',3),
               V = np.array([])):

    """
    INTERP3SPH interpolates y at Xq,Yq,Zq using the 3D kernel W centered on centers

   Syntax:
       Vq = interp3SPH(X,y,Xq,Yq,Zq [,W,V])

   Inputs:
     centers : kx3 coordinates of the kernel centers
           y : kxny values at X (m is the number of values associated with the same center)
               [] (empty matrix) forces a uniform density calculatoin
          Xq : array or matrix coordinates along X
          Yq : array or matrix coordinates along Y
          Zq : array or matrix coordinates along Z
           W : kernel function @(r) <-- use kernelSPH() to supply a vectorized kernel
           V : kx1 volume of the kernels (default=1)
               [] (empty matrix) or scalar value forces uniform volumes (default =1)

   Output:
           Vq : same size as Xq, with an additional dimension if y was an array

    Example:  arbitrary field to be interpolated x+2*y-3*z

        import numpy as np
        import matplotlib.pyplot as plt
        from mpl_toolkits.mplot3d import Axes3D
        from scipy.interpolate import griddata

        from utils.SPHtools import interp3SPH


        r = 0.5
        h = 2*r
        XYZ = packSPH(5,r)
        W = kernelSPH(h,'lucy',3)
        y = XYZ @ np.array([1,2,-3]).transpose()
        nresolution = 50
        xg = np.linspace(np.min(XYZ[:,0])-h,np.max(XYZ[:,0])+h,num=nresolution)
        yg = np.linspace(np.min(XYZ[:,1])-h,np.max(XYZ[:,1])+h,num=nresolution)
        zg = np.linspace(np.min(XYZ[:,2])-h,np.max(XYZ[:,2])+h,num=nresolution)
        Xg,Yg,Zg = np.meshgrid(xg,yg,zg)
        Vg = interp3SPH(XYZ,y,Xg,Yg,Zg,W)

        # projection along y,z
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(Xg[1,:,1],np.mean(Vg,axis=(0,2),keepdims=False),color='red',marker='o')

        # unvalidated code for voxels
        fig = plt.figure()
        cmap = plt.cm.get_cmap("RdPu_r", 64)
        ax = fig.add_subplot(111, projection='3d')
        ax.set_box_aspect([1,1,1]) # set aspect ratio of the 3D plot
        hs = ax.contour(Xg, Yg, Zg, Vg, 10, cmap=cmap) # not working
        fig.colorbar(hs, ax=ax)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        plt.show()

   See also: interp2SPH, kernelSPH, packSPH

    """

    # 2023-02-20 | INRAE\Olivier Vitrac, Han Chen | rev. 2023-02-21

    # arg check
    if isinstance(centers,list): centers = np.array(centers)
    k,d = centers.shape
    ky,ny = np.shape(y) if np.ndim(y)>1 else (np.size(y),1)
    kv = np.size(V)
    if k==0: raise ValueError('please supply some centers')
    if d != 3: raise ValueError('3 dimensions (columns) are required')
    if ky*ny==0: y = np.ones(k,1); ky=k; ny=1;
    if ky != k: raise ValueError(f'the number of y values ({ky}) does not match the number of kernels ({k})')
    if Xq.shape != Yq.shape  or Yq.shape != Zq.shape: raise ValueError('Xq,Yq and Zq do not have compatible sizes')
    if kv==0:  V=1;  kv=1;
    if kv==1: V = np.ones([k,1])*V; kv=k;
    if kv!=k: raise ValueError(f'the number of V values ({kv}) does not match the number of kernels ({k})')

    # main
    sumW = [];
    verbosity = np.size(Xq)>1e4;
    for i in range(k):
        # initialization if needed
        if i==0:
            for iy in range(ny):
                sumW.append(np.zeros(np.shape(Xq),dtype=Xq.dtype))
        # interpolation
        if verbosity:print(f'interpolate respectively to kernel {i} of {k}')
        R = np.sqrt( (Xq-centers[i,0])**2 + \
                     (Yq-centers[i,1])**2 + \
                     (Zq-centers[i,2])**2 )
        if np.ndim(y)==1:
            sumW[0] = sumW[0] + y[i] * V[i] * W(R);
        else:
            for iy in range(ny):
                sumW[iy] = sumW[iy] + y[i,iy] * V[i] * W(R);

    # output (data unfolding)
    if ny==1:
        return sumW[0];
    else:
        return np.stack(sumW,axis=Xq.ndim)