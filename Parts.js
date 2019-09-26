const math = require('mathjs')
const Axis = Object.freeze({"X":1, "Y":2, "Z":3})

class Movements {
    constructor() {}
    
    rotaion_axis_matrix(degrees, axis) {
        switch (axis) {
            case Axis.X:
                return math.matrix([
                            [1, 0, 0],
                            [0, math.cos(math.unit(degrees, 'deg')), -math.sin(math.unit(degrees, 'deg'))],
                            [0, math.sin(math.unit(degrees, 'deg')), math.cos(math.unit(degrees, 'deg'))]])
            case Axis.Y:
                return math.matrix([
                            [math.cos(math.unit(degrees, 'deg')), 0, -math.sin(math.unit(degrees, 'deg'))],
                            [0, 1, 0],
                            [math.sin(math.unit(degrees, 'deg')), 0, math.cos(math.unit(degrees, 'deg'))]])
            case Axis.Z:
                return math.matrix([
                            [math.cos(math.unit(degrees, 'deg')), -math.sin(math.unit(degrees, 'deg')), 0],
                            [math.sin(math.unit(degrees, 'deg')), math.cos(math.unit(degrees, 'deg')), 0],
                            [0, 0, 1]])
        }
    }
    
    rotation_matrix(A,B) {
        return math.dotMultiply(A, B)
    }
}

class Joint extends Movements {
    constructor(location, theta, link) {
        self.location = location
        self.theta = theta
        self.link = link
    }
    
    rotate_link(theta, axis) {
        if self.link != null {
            self.link.rotate_link(theta, axis)
        }
        
        self.theta += theta
    }
    
    set_theta(theta, axis) {
        if self.link != null {
            self.link.set_theta(theta, axis)
        }
        
        self.theta = theta
    }
    
    set_location(location) {
        if self.link != null {
            self.link.set_base_joint(location)
        }
        
        self.location = location
    }
    
    get_link() {
        return self.link
    }
}

class Link extends Movements {
    constructor(length, base_joint, end_joint) {
        self.length = length
        self.base_joint = base_joint
        
        if end_joint != null {
            self.end_joint = end_joint
        } else {
            self.end_joint = Joint(math.matrix([base_joint.location[0]+length, 0, 0]))
        }
    }
    
    set_theta(theta, axis) {
        self.end_joint.rotate_link(-self.end_joint.theta+theta, axis)
    }
    
    set_base_joint(location) {
        self.end_joint.set_location(math.add(math.subtract(location, self.base_joint.location), self.end_joint.location))
    }
    
    rotate_link(degrees, axis) {
        const rotation = rotaion_axis_matrix(degrees, axis)
        self.end_joint.set_location(math.dotMultiply(self.end_joint.location, rotation))
    }
    
    get_arm_locations() {
        return (self.base_joint.location, self.end_joint.location)
    }
}
