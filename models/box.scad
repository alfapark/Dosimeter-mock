use <radiation.scad>
use <signal.scad>

// shear such that point will translate by [p.x,p.y] as z-axis is traversed by p.z units
// https://gist.github.com/thehans/c30c259e83da4e89ccbd975a511dab68
module shearAlongZ(p) {
  multmatrix([
    [1,0,p.x/p.z,0],
    [0,1,p.y/p.z,0],
    [0,0,1,0]
  ]) children();
}

module box_upper(
size_x, // x size of the lid
size_y, // y size of the lid
thickness, // thickness of the lid
screw_offset, // both x and y offset for screw hole from the corner to the center of the hole
screw_hole_size,
rectangle_holes, // array of [x,y, size_x, size_y] - x,y is the ofset to the left upper corner
circle_holes, // array of [x,y, diameter] - x,y is the offset from center
pegs, // array of [x,y, size_x, size_y, size_z, shear_x, shear_y]
bridges, // array of [x,y,size_x,size_y,size_z]
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
            translate([object[0]+offset_x, object[1]+offset_y,-object[4]])
                cube([object[2], object[3], thickness]);
        }
        for(object = circle_holes){
            translate([object[0]+offset_x, object[1]+offset_y,0])
                cylinder(h=thickness, d=object[2]);
        }
        
        /* Not printable for now */
        translate([offset_x, offset_y, thickness])
            mirror([0,0,1])
                children();
    }
    for(peg = pegs){
        translate([peg[0]+offset_x-peg[5], peg[1]+offset_y-peg[6], -peg[4]])
        shearAlongZ([peg[5],peg[6],peg[4]])
            cube([peg[2], peg[3], peg[4]]);
    }
    for(bridge = bridges){
        translate([bridge[0]+offset_x, bridge[1]+offset_y-thickness, -bridge[4]]){
                cube([bridge[2], thickness, bridge[4]]);
            translate([0,0,-thickness])
                cube([bridge[2], bridge[3]+2*thickness, thickness]);
            translate([0, bridge[3]+thickness, 0])
                cube([bridge[2], thickness, bridge[4]]);
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
    walls, // array of [x,y, size_x, size_y, size_z] - x,y is the offset to the left upper corner,
    columns, // array of [x,y, diameter, height]
    antenna_width,
    antenna_height
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
    
    for(object = columns){
        translate([object[0]+offset_x, object[1]+offset_y, offset_z])
            cylinder(d = object[2], h = object[3]);
    }
    // anntenna
    translate([0, new_y,0]){
        difference(){
            cube([antenna_width+thickness, antenna_width+thickness, antenna_height+thickness]);
            translate([(antenna_width+thickness)/2,(antenna_width+thickness)/2, thickness])
            cylinder(d=antenna_width, h=antenna_height);
        }
    }
}
size_x = 125;
size_y = 150;
translate([0,0, 200])
box_upper(
size_x=size_x,
size_y=size_y,
thickness=2.5,
screw_offset=5,
screw_hole_size=5,
rectangle_holes=[
    [80, 120, 31, 14.5,0], // display
    [90, 40, 12, 12,0], // button 
    [10, 10, 43, 61, 1.5] // NFC 
], 
circle_holes=[
    [60,90,6], // HP
    [70,90,6],
    [80,90,6],
    [90,90,6],
    [100,90,6],
    [110,90,6],
    [110,105,6], // status
    [30, 120,6], // radiation
],
pegs=[
    [7.5,20, 3,3, 5, 5, 0], // NFC
    [53,20, 3,3, 5, -5, 0],
    [7.5,55, 3,3, 5, 5, 0],
    [53,55, 3,3, 5, -5, 0],
    [80, 120-3, 31, 3, 4,0,0], // display support
    [80+31, 120-3, 3, 14+6, 4,0,0], 
    [80, 120+14, 31, 3, 4,0,0], 
],
bridges=[
    [80, 43, 4, 6, 3], // button 
    [108, 43, 4, 6,3], // button 
]
){
    linear_extrude(height=0.5)
        translate([30, 120])
            radiation(25, 5, 3);
    linear_extrude(height=0.5)
        translate([31, 40])
            signal(4, 3);};
// calculating mounting for rpi
rpi_screw1_x = 10;
rpi_screw1_y = 146;
rpi_length = 85;
rpi_width = 56;
rpi_screw_to_side = 4;
rpi_wall_x = rpi_screw1_x-rpi_screw_to_side+rpi_length;
rpi_wall_y = rpi_screw1_y+rpi_screw_to_side-rpi_width;
box_lower(
size_x=size_x,
size_y=size_y,
size_z =40,
thickness=2.5,
screw_offset=5,
screw_hole_size=3,
walls=[
    [size_x-91-2.5, 0, 2.5, 20, 22], // powerbank short
    [size_x-90,44,91,2.5,22], // powerbank long
    [rpi_wall_x, rpi_wall_y, 2.5, 150-(rpi_wall_y), 3], // rpi vertical mini wall
    [0, rpi_wall_y-2.5, rpi_wall_x+2.5, 2.5, 3], // rpi horizontal mini wall
],
columns=[
    [rpi_screw1_x,rpi_screw1_y,2.7,5], // RPI screw columns
    [rpi_screw1_x+58,rpi_screw1_y,2.7,5],
    [rpi_screw1_x,rpi_screw1_y-49,2.7,5],
    [rpi_screw1_x+58,rpi_screw1_y-49,2.7,5]
],
antenna_width=10,
antenna_height=10
);