// Gmsh project created on Wed Apr 24 21:05:29 2019
SetFactory("OpenCASCADE");
//+
Rectangle(1) = {-1, -0, 0, 1, 0.5, 0};
//+
Physical Curve("lewa") = {4};
//+
Physical Curve("prawa") = {2};
//+
Physical Curve("gora") = {3};
//+
Physical Curve("dol") = {1};
//+
Physical Surface("internal") = {1};
