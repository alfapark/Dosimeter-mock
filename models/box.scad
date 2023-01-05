module box_upper(
size_x, // x size of the lid
size_y, // y size of the lid
thickness, // thickness of the lid
screw_offset, // both x and y offset for screw hole from the corner to the center of the hole
screw_hole_size,
rectangle_holes, // array of [x,y, size_x, size_y] - x,y is the ofset to the left upper corner
circle_holes, // array of [x,y, diameter] - x,y is the offset from center

){
    new_x=size_x+2*thickness;
    new_y=size_y+4*screw_offset;
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
            translate([object[0], object[1],0])
                cube([object[2], object[3], thickness]);
        }
        for(object = circle_holes){
            translate([object[0], object[1],0])
                cylinder(h=thickness, d=object[2]);
        }
    }
}

module box_lower(

){
}

box_upper(
size_x=125,
size_y=150,
thickness=2.5,
screw_offset=5,
screw_hole_size=5,
rectangle_holes=[
    [80, 130, 30, 14], // display
    [90, 50, 12, 12] //button 
], 
circle_holes=[
    [20,90,4.5], // status
    [50,90,4.5], 
    [60,90,4.5],
    [70,90,4.5],
    [80,90,4.5],
    [90,90,4.5],
    [100,90,4.5]
]
);