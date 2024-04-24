function circleFit = fitCircleFromPoints(XY)
%FITCIRCLEFROMPOINTS fit a circle from a set of points and calculate the missing information such as the radius, centroid, and angles
%
%   Syntax: circleFit = fitCircleFromPoints(XY)
%       XY is a Nx2 matrix where N is the number of points
%       circleFit is a structure with fields
%           center: [xcenter y center]
%           radius: radius
%         minAngle: minimum angle
%         maxAngle: maximum angle
%           angles: corresponding angles
%      XYgenerator: returns the position XY from an angles
%   angleGenerator: returns the angles from positions XY

% MS 3.0 | 2024-03-23 | INRAE\han.chen@inrae.fr, INRAE\Olivier.vitrac@agroparistech.fr | rev. 


% Revision history



% Initial estimate of the center using the centroid of the points
initialCenter = mean(XY, 1);

% Define the objective function for the least squares problem
objectiveFunction = @(params) sum(((XY(:,1) - params(1)).^2 + (XY(:,2) - params(2)).^2 - params(3)^2).^2);

% Initial guess for [center_x, center_y, radius]
initialGuess = [initialCenter, sqrt(var(XY(:,1)) + var(XY(:,2)))];

% Optimize using fminsearch or another optimization function
optimizedParams = fminsearch(objectiveFunction, initialGuess);

% Extract the optimized center and radius
center = optimizedParams(1:2);
radius = optimizedParams(3);

% Calculate shifted points and angles
XY_shifted = XY - center;
angles = atan2(XY_shifted(:,2), XY_shifted(:,1));

% Calculate the full angle range of the given points
minAngle = min(angles);
maxAngle = max(angles);

% Return results in a structure
circleFit.center = center;
circleFit.radius = radius;
circleFit.minAngle = minAngle;
circleFit.maxAngle = maxAngle;
circleFit.angles = angles;
circleFit.XYgenerator = @(a) [cos(a(:)) sin(a(:))]*radius + center;
circleFit.angleGenerator = @(xy) atan2(xy(:,2)-center(2), xy(:,1)-center(1));