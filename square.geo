// Gmsh project created on Fri Apr 19 23:32:22 2019

//+
SetFactory("OpenCASCADE");
Rectangle(1) = {0, -0, 0, 1, 1, 0};
//+
Physical Curve(1) = {1};
//+
Physical Curve(2) = {2};
//+
Physical Curve(3) = {3};
//+
Physical Curve(4) = {4};
//+
Physical Surface(5) = {1};
//+
Transfinite Curve {1, 4, 2, 3} = 10 Using Progression 1;
//+
Transfinite Surface {1};
//+
Recombine Surface {1};
