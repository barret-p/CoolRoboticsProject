// const Kinematics = require('kinematics').default

// const geometry = [
//       [1,  1,  0], // V0: 1x 1y
//       [0, 10,  0], // V1: 10y
//       [5,  0,  0], // V2: 5x
//       [3,  0,  0], // V3: 3x
//       [0, -3,  0], // V4: -3y
//     ]

// const RobotKin = new Kinematics(geometry)

// let angles = [1.57, 1.2, 0, 0.3, 2.2, 1.1]

// const pose = RobotKin.forward(...angles)[5]

// angles = RobotKin.inverse(...pose)

// const math = require('mathjs')
// const Axis = Object.freeze({"X":1, "Y":2, "Z":3})

// class Movements {
//     constructor() {}
    
//     rotaion_axis_matrix(degrees, axis) {
//         switch (axis) {
//             case Axis.X:
//                 return math.matrix([
//                             [1, 0, 0],
//                             [0, math.cos(math.unit(degrees, 'deg')), -math.sin(math.unit(degrees, 'deg'))],
//                             [0, math.sin(math.unit(degrees, 'deg')), math.cos(math.unit(degrees, 'deg'))]])
//             case Axis.Y:
//                 return math.matrix([
//                             [math.cos(math.unit(degrees, 'deg')), 0, -math.sin(math.unit(degrees, 'deg'))],
//                             [0, 1, 0],
//                             [math.sin(math.unit(degrees, 'deg')), 0, math.cos(math.unit(degrees, 'deg'))]])
//             case Axis.Z:
//                 return math.matrix([
//                             [math.cos(math.unit(degrees, 'deg')), -math.sin(math.unit(degrees, 'deg')), 0],
//                             [math.sin(math.unit(degrees, 'deg')), math.cos(math.unit(degrees, 'deg')), 0],
//                             [0, 0, 1]])
//         }
//     }
    
//     rotation_matrix(A,B) {
//         return math.dotMultiply(A, B)
//     }
// }

// class Joint extends Movements {
//     constructor(location, theta, link) {
//         self.location = location
//         self.theta = theta
//         self.link = link
//     }
    
//     rotate_link(theta, axis) {
//         if (self.link != null) {
//             self.link.rotate_link(theta, axis)
//         }
        
//         self.theta += theta
//     }
    
//     set_theta(theta, axis) {
//         if (self.link != null) {
//             self.link.set_theta(theta, axis)
//         }
        
//         self.theta = theta
//     }
    
//     set_location(location) {
//         if (self.link != null) {
//             self.link.set_base_joint(location)
//         }
        
//         self.location = location
//     }
    
//     get_link() {
//         return self.link
//     }
// }

// class Link extends Movements {
//     constructor(length, base_joint, end_joint) {
//         self.length = length
//         self.base_joint = base_joint
        
//         if (end_joint != null) {
//             self.end_joint = end_joint
//         } else {
//             self.end_joint = Joint(math.matrix([base_joint.location[0]+length, 0, 0]))
//         }
//     }
    
//     set_theta(theta, axis) {
//         self.end_joint.rotate_link(-self.end_joint.theta+theta, axis)
//     }
    
//     set_base_joint(location) {
//         self.end_joint.set_location(math.add(math.subtract(location, self.base_joint.location), self.end_joint.location))
//     }
    
//     rotate_link(degrees, axis) {
//         const rotation = rotaion_axis_matrix(degrees, axis)
//         self.end_joint.set_location(math.dotMultiply(self.end_joint.location, rotation))
//     }
    
//     get_arm_locations() {
//         return (self.base_joint.location, self.end_joint.location)
//     }
// }
function rotationMatrix(theta1, theta2, theta3) {
    
}

// functions to rotate tha arms
function rotateClockwise(link, linkOrigin) {
    link.rotate(1, linkOrigin[0], linkOrigin[1]);
}

function rotateCounterClockwise(link, linkOrigin) {
    link.rotate(-1, linkOrigin[0], linkOrigin[1]);
}

anychart.onDocumentLoad(function () {
    
    // initialize drawing area
    var stage = acgraph.create('drawing-area');
    var windowBorder = stage.rect(0,0, 600, 600);

    // create base
    var baseOrigin = [300, 600];
    var baseDimension = [10,10];
    var base = stage.rect(baseOrigin[0] - baseDimension[0]/2, baseOrigin[1] - baseDimension[1], baseDimension[0], baseDimension[1]);

    // create joint 1
    var joint1;
    var link1Origin = [300, 600];
    var link1Dimension = [6, 150];
    var link1 = stage.rect(link1Origin[0], link1Origin[1], link1Dimension[0], link1Dimension[1]);
    link1.fill('blue');
    link1.rotate(180, link1Origin[0], link1Origin[1]);

    // joint 1 button functions
    $("#link1clockwise").click(function() {
        rotateClockwise(link1, link1Origin);
    });

    $("#link1counterclockwise").click(function() {
        rotateCounterClockwise(link1, link1Origin);
    });

    // create joint 2
    var joint2;
    var link2Origin = [300,450];
    var link2Dimension = [6, 100];
    var link2 = stage.rect(link2Origin[0], link2Origin[1], link2Dimension[0], link2Dimension[1]);
    link2.fill('red');
    link2.rotate(180, link2Origin[0], link2Origin[1]);

    // joint 2 button functions
    $("#link2clockwise").click(function() {
        rotateClockwise(link2, link2Origin);
    });

    $("#link2counterclockwise").click(function() {
        rotateCounterClockwise(link2, link2Origin);
    });

    // create joint 3
    var joint3;
    var link3Origin = [300, 350];
    var link3Dimension = [6, 75];
    var link3 = stage.rect(link3Origin[0], link3Origin[1], link3Dimension[0], link3Dimension[1]);
    link3.fill('green');
    link3.rotate(180, link3Origin[0], link3Origin[1]);

    // joint 3 button functions
    $("#link3clockwise").click(function() {
        rotateClockwise(link3, link3Origin);
    });

    $("#link3counterclockwise").click(function() {
        rotateCounterClockwise(link3, link3Origin);
    });

    // create paintbrush
    var paintBrushOrigin = [300, 100];
    var paintBrushDimension = 10;
    var paintBrush = stage.circle(paintBrushOrigin[0], paintBrushOrigin[1], paintBrushDimension);

    });