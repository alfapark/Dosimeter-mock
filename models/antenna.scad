module antenna(big_radius, small_radius, mounting_height, cone_height, upper_height){
    cylinder(r=big_radius, h=mounting_height);
    translate([0,0,mounting_height])
        cylinder(r1=big_radius, r2=small_radius, h=cone_height);
    translate([0,0,mounting_height+cone_height])
        cylinder(r=small_radius, h=upper_height);
    translate([0,0,mounting_height+cone_height+upper_height])
        sphere(r=small_radius);
}

antenna(9.9, 5, 10, 80, 20);