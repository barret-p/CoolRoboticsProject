using UnityEngine;

public class PointInTime
{
    public Vector3 position;
    public Vector3 rotation;
    public float Vfr;
    public float SWrotation;

    public PointInTime(Vector3 _position, Vector3 _rotation, float _Vfr, float _SWrotation)
    {
        position = _position;
        rotation = _rotation;
        Vfr = _Vfr;
        SWrotation = _SWrotation;
    }
}
