// Gmsh project created on Sat Apr 20 17:47:32 2019
SetFactory("OpenCASCADE");
//+
Point(1) = {0.9, -1.8, 0, 1.0};
//+
Point(2) = {1.9, -1.8, 0, 1.0};
//+
Point(3) = {1.9, -0.8, 0, 1.0};
//+
Point(4) = {0.9, -0.8, 0, 1.0};
//+
Point(5) = {1.2, -1.1, 0, 1.0};
//+
Line(1) = {1, 2};
//+
Line(2) = {2, 3};
//+
Line(3) = {3, 4};
//+
Line(4) = {4, 5};
//+
Line(5) = {5, 1};
//+
Curve Loop(1) = {5, 1, 2, 3, 4};
//+
Plane Surface(1) = {1};
//+
Physical Curve(1) = {5};
//+
Physical Curve(2) = {1};
//+
Physical Curve(3) = {2};
//+
Physical Curve(4) = {3};
//+
Physical Curve(5) = {4};
//+
Physical Surface(6) = {1};
