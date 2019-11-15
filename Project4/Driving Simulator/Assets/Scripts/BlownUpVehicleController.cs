using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class BlownUpVehicleController : MonoBehaviour
{
    public GameObject steeringwheel;
    public GameObject FRWheel;
    public GameObject FLWheel;
    public GameObject RealCar;

    public int g;
    public int d;

    void FixedUpdate()
    {
        Vector3 temp = RealCar.gameObject.transform.rotation.eulerAngles;
        temp.z -= 90;
        transform.rotation = Quaternion.Euler(temp);

        var rotationVector = transform.rotation.eulerAngles;
        float oldZ = rotationVector.z;

        rotationVector.z -= RealCar.gameObject.GetComponent<VehicleController>().alphaR;
        FRWheel.transform.rotation = Quaternion.Euler(rotationVector);
        rotationVector.z = oldZ;

        rotationVector.z -= RealCar.gameObject.GetComponent<VehicleController>().alphaL;
        FLWheel.transform.rotation = Quaternion.Euler(rotationVector);
    }
}
