# packSPH()

**Function**: `X = packSPH(siz, r, typ)`

**Purpose**: This function returns the Hexagonal Close Packing (HCP) or Face-Centered Cubic (FCC) packing of spheres, which are common arrangements in crystal structures or packing problems.

### Inputs:
1. `siz`: A vector specifying the number of spheres along the x, y, z dimensions. If `siz` is a scalar, the same value is applied to all three dimensions (e.g., `[siz siz siz]`).
2. `r`: The radius of the beads or spheres.
3. `typ`: Specifies the type of packing. Can be either 'HCP' (default, with a period of 2) or 'FCC' (with a period of 3).

### Output:
- `X`: A matrix of dimensions `[size(1) x size(2) x size(3)] x 3` representing the centers of the spheres in the packing arrangement.

### Example Usage:
- `X = packSPH(5)`: This would generate an HCP packing of 5 spheres along each dimension with default settings.

### Related Functions:
- `interp3SPH`, `interp2SPH`, `kernelSPH`

