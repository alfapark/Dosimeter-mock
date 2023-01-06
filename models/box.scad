module box_upper(
size_x, // x size of the lid
size_y, // y size of the lid
thickness, // thickness of the lid
screw_offset, // both x and y offset for screw hole from the corner to the center of the hole
screw_hole_size,
rectangle_holes, // array of [x,y, size_x, size_y] - x,y is the ofset to the left upper corner
circle_holes, // array of [x,y, diameter] - x,y is the offset from center

){
    offset_x = thickness;
    offset_y = 2*screw_offset;
    new_x=size_x+2*offset_x;
    new_y=size_y+2*offset_y;
    difference(){
        union(){
            cube([size_x+2*thickness, size_y+4*screw_offset, thickness]);
            //brim
            translate([thickness,2*screw_offset,-thickness])
            difference(){
                    cube([size_x, size_y, thickness]);
                    translate([thickness, thickness,0])
                    cube([size_x-2*thickness, size_y-2*thickness, thickness]);
            }
        }
        // screw holes
        for(screw_x = [screw_offset, new_x-screw_offset]){
            for(screw_y = [screw_offset, new_y - screw_offset]){
                translate([screw_x, screw_y, 0])
                    cylinder(h = thickness, d = screw_hole_size);
            }
        }
        // other holes
        for(object = rectangle_holes){
            translate([object[0]+offset_x, object[1]+offset_y,0])
                cube([object[2], object[3], thickness]);
        }
        for(object = circle_holes){
            translate([object[0]+offset_x, object[1]+offset_y,0])
                cylinder(h=thickness, d=object[2]);
        }
    }
}

module box_lower(
    size_x, // x size of the box
    size_y, // y size of the box
    size_z, // z size (height) of the box
    thickness, // thickness of the lid
    screw_offset, // both x and y offset for screw hole from the corner to the center of the hole
    screw_hole_size,
    walls, // array of [x,y, size_x, size_y, size_z] - x,y is the offset to the left upper corner
){
    offset_x = thickness;
    offset_y = 2*screw_offset;
    offset_z = thickness;
    new_x=size_x+2*offset_x;
    new_y=size_y+2*offset_y;
    new_z=size_z+offset_z;
    difference(){
        cube([new_x, new_y, new_z]);
        translate([thickness, 2*screw_offset, thickness])
            cube([size_x, size_y, size_z]);
        // screw holes
        for(screw_x = [screw_offset, new_x-screw_offset]){
            for(screw_y = [screw_offset, new_y - screw_offset]){
                translate([screw_x, screw_y, 0])
                    cylinder(h = new_z, d = screw_hole_size);
            }
        }
    }
    for(object = walls){
        translate([object[0]+offset_x, object[1]+offset_y, offset_z])
            cube([object[2], object[3], object[4]]);
    }
}
translate([0,0, 200])
box_upper(
size_x=125,
size_y=150,
thickness=2.5,
screw_offset=5,
screw_hole_size=5,
rectangle_holes=[
    [80, 120, 30, 14], // display
    [90, 40, 12, 12] //button 
], 
circle_holes=[
    [20,80,4.5], // status
    [50,80,4.5], // HP
    [60,80,4.5],
    [70,80,4.5],
    [80,80,4.5],
    [90,80,4.5],
    [100,80,4.5]
]
);

box_lower(
size_x=125,
size_y=150,
size_z =40,
thickness=2.5,
screw_offset=5,
screw_hole_size=5,
walls=[
    [125-91-2.5, 0, 2.5, 20, 22], // powerbank short
    [125-90,43,91,2.5,22]
]
);