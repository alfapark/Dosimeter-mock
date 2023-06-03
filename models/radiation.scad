module radiation(radius,inner_radius,border){
    for(r = [0,120,240]){
        rotate(r)
            difference(){
                intersection(){
                    circle(radius);
                    square(radius);
                    rotate(30)
                        square(radius);
                }
                circle(inner_radius+border);
            }
    }
    circle (inner_radius);
}

radiation(20,3,2);                 