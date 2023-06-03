module signal(width, k){
    difference(){
    for(i = [1:k]){
        difference([]){
            circle(width*(i*2+1));
            circle(width*(i*2));
        }
    }
    square(width*k*4);
    mirror([1,1])
    square(width*k*4);
    }
    circle (width);
}

signal(10, 3);