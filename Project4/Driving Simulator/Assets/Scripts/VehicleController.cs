using System.Collections;
using System.Collections.Generic;
using UnityEngine;
using UnityEngine.UI;

public class VehicleController : MonoBehaviour
{
    public GameObject Track;
    public GameObject steeringwheel;
    public GameObject FRWheel;
    public GameObject FLWheel;

    public bool recording;
    public bool playing;
    public int frameCount;
    public int CurrentFrame;
    public int i;
    public int g;
    public int d;
    public float Vfr;
    public float Vfl;
    public float Vbr;
    public float Vbl;
    public float r;
    public float omega;
    public float V;
    public float alphaR;
    public float alphaL;

    public float movementSpeed;

    public Text VfrText;
    public Text VflText;
    public Text VbrText;
    public Text VblText;
    public Text VelocityText;
    public Text VfrControlText;

    public GameObject top;
    public GameObject bottom;

    public float ScaleFactor;
    public GameObject BlownupTrack;

    public GameObject Record;
    public GameObject Pause;
    public GameObject Play;

    public GameObject myPrefab;


    List<PointInTime> pointsInTime;
    List<GameObject> Trails;


    // Start is called once at the start
    void Start()
    {
        Screen.SetResolution(1280, 720, false);
        pointsInTime = new List<PointInTime>();
        recording = false;
        playing = false;
        i = 0;
        Record.GetComponent<SpriteRenderer>().enabled = false;
        Pause.GetComponent<SpriteRenderer>().enabled = false;
        Play.GetComponent<SpriteRenderer>().enabled = false;

        Trails = new List<GameObject>();
        for(int j = 0; j < 300; j++)
        {
            Trails.Add(Instantiate(myPrefab, new Vector3(0, 6, 0), Quaternion.identity));
        }
    }

    float map(float s, float a1, float a2, float b1, float b2)
    {
        return b1 + (s - a1) * (b2 - b1) / (a2 - a1);
    }

    float calculateAlphaR(float angle)
    {
        if (angle > 0)
        {
            angle = map(angle, 0, 200, 0, 30);
        }
        else if (angle < 0)
        {
            angle = map(angle, -200, 0, -22.98952f, 0);
        }
        return angle;
    }

    float calculateR(float angle)
    {
        return (g / Mathf.Tan(Mathf.Deg2Rad * angle)) + d;
    }

    float calculateAlphaL(float angle)
    {
        return Mathf.Rad2Deg * Mathf.Atan(g / (calculateR(angle) + d));
    }

    float calculateOmega(float Vfr, float alphaR)
    {
        return Vfr * Mathf.Sin(Mathf.Deg2Rad * alphaR) / g;
    }

    float calculateVfl(float omega, float alphaL, float Vfr)
    {
        if(omega == 0f)
        {
            return Vfr;
        }
        return (omega * g) / Mathf.Sin(Mathf.Deg2Rad * alphaL);
    }

    float calculateVbr(float omega, float r, float Vfr)
    {
        if(omega == 0)
        {
            return Vfr;
        }
        return omega * (r - d);
    }

    float calculateVbl(float omega, float r, float Vfr)
    {
        if (omega == 0)
        {
            return Vfr;
        }
        return omega * (r + d);
    }

    float calculateV(float Vfr, float omega, float r)
    {
        if(omega == 0)
        {
            return Vfr;
        }
        else
        {
            return omega * r;
        }
    }

    public void LowerSpeed()
    {
        if (Vfr > -5)
        {
            Vfr -= 5;
        }
    }

    public void IncreaseSpeed()
    {
        if (Vfr < 200)
        {
            Vfr += 5;
        }
    }



    private void Update()
    {
        if (Input.GetKeyDown("="))
        {
            IncreaseSpeed();
        }
        else if (Input.GetKeyDown("-"))
        {
            LowerSpeed();
        }
        else if (Input.GetKeyDown("]"))
        {
            Vfr = 200;
        }
        else if (Input.GetKeyDown("["))
        {
            Vfr = 0;
        }
        else if (Input.GetKeyDown("r"))
        {
            if (recording)
            {
                Record.GetComponent<SpriteRenderer>().enabled = false;
                recording = false;
            }
            else if(!playing)
            {
                Record.GetComponent<SpriteRenderer>().enabled = true;
                recording = true;
                if(pointsInTime.Count > 0)
                {
                    for(int j = pointsInTime.Count-1; j >= 0; j--)
                    {
                        pointsInTime.RemoveAt(j);
                    }
                    for(int j = 0; j < Trails.Count; j++)
                    {
                        Trails[j].transform.position = new Vector3(0, 6, 0);
                    }
                }
            }
        }
        else if (Input.GetKeyDown("p"))
        {
            if (playing)
            {
                Play.GetComponent<SpriteRenderer>().enabled = false;
                playing = false;
            }
            else
            {
                if (!recording)
                {
                    Play.GetComponent<SpriteRenderer>().enabled = true;
                    recording = false;
                    playing = true;
                    i = 0;
                }
            }
        }
        else if (Input.GetKeyDown(KeyCode.Escape))
        {
            Application.Quit();
        }

    }

    // FixedUpdate is called 50 times a second
    void FixedUpdate()
    {
        Vector3 positionVector = transform.position;
        Vector3 rotationVector = transform.rotation.eulerAngles;

        float SWRotation = steeringwheel.GetComponent<SteeringWheel>().GetAngle();
        Pause.GetComponent<SpriteRenderer>().enabled = false;
        Play.GetComponent<SpriteRenderer>().enabled = false;

        if (playing)
        {
            steeringwheel.GetComponent<SteeringWheel>().enabled = false;
            positionVector = pointsInTime[i].position;
            rotationVector = pointsInTime[i].rotation;
            Vfr = pointsInTime[i].Vfr;
            SWRotation = pointsInTime[i].SWrotation;
            Vector3 rot = new Vector3(0, 0, -SWRotation);
            steeringwheel.GetComponent<SteeringWheel>().gameObject.transform.rotation = Quaternion.Euler(rot);
            transform.rotation = Quaternion.Euler(rotationVector);
            transform.position = positionVector;
            Play.GetComponent<SpriteRenderer>().enabled = false;
            Pause.GetComponent<SpriteRenderer>().enabled = true;
            if (i < pointsInTime.Count - 1)
            {
                Play.GetComponent<SpriteRenderer>().enabled = true;
                Pause.GetComponent<SpriteRenderer>().enabled = false;
                i++;
            }
        }
        else if(!playing)
        {
            steeringwheel.GetComponent<SteeringWheel>().enabled = true;
            SWRotation = steeringwheel.GetComponent<SteeringWheel>().GetAngle();

            if (omega != 0 && Vfr != 0)
            {
                Vector3 pos = positionVector;
                pos.x += r / ScaleFactor / 64 * Mathf.Cos(Mathf.Deg2Rad * rotationVector.z); // scale it relative to the world
                pos.y += r / ScaleFactor / 64 * Mathf.Sin(Mathf.Deg2Rad * rotationVector.z);
                Debug.DrawLine(positionVector, pos);
                transform.RotateAround(pos, new Vector3(0, 0, 1), Mathf.Rad2Deg * -Time.deltaTime * V / ScaleFactor / (r / ScaleFactor / 64));
            }
            else if (omega == 0 && Vfr != 0)
            {
                Vector3 pos2 = positionVector;
                pos2.x += V / ScaleFactor * Mathf.Cos(Mathf.Deg2Rad * (rotationVector.z + 90)) * Time.deltaTime;
                pos2.y += V / ScaleFactor * Mathf.Sin(Mathf.Deg2Rad * (rotationVector.z + 90)) * Time.deltaTime;
                transform.position = pos2;
            }


            if (recording)
            {
                pointsInTime.Add(new PointInTime(positionVector, rotationVector, Vfr, SWRotation));
                if(frameCount % 50 == 0)
                {
                    Trails[(frameCount / 50)].transform.position = positionVector;
                }
            }
        }

        CurrentFrame = i;
        frameCount = pointsInTime.Count;

        float oldZ = rotationVector.z;

        float angle = SWRotation;
        alphaR = calculateAlphaR(angle);
        alphaL = calculateAlphaL(alphaR);

        rotationVector.z += -alphaR;
        FRWheel.transform.rotation = Quaternion.Euler(rotationVector);
        rotationVector.z = oldZ;

        rotationVector.z += -alphaL;
        FLWheel.transform.rotation = Quaternion.Euler(rotationVector);
        rotationVector.z = oldZ;

        omega = calculateOmega(Vfr, alphaR);
        Vfl = calculateVfl(omega, alphaL, Vfr);
        r = calculateR(alphaR);
        Vbr = calculateVbr(omega, r, Vfr);
        Vbl = calculateVbl(omega, r, Vfr);
        V = calculateV(Vfr, omega, r);

        VelocityText.text = "Velocity: " + V.ToString("0.##");
        VfrControlText.text = "Vfr: " + Vfr.ToString();
        VfrText.text = Vfr.ToString("0.##");
        VflText.text = Vfl.ToString("0.##");
        VbrText.text = Vbr.ToString("0.##");
        VblText.text = Vbl.ToString("0.##");


        float y = -((Track.gameObject.transform.position.x - positionVector.x) * 15) - 0.41f;
        float x = ((Track.gameObject.transform.position.y - positionVector.y) * 15) - 1.71f;
        Vector3 track = new Vector3(0,0,0);
        track.x = x;
        track.y = y;
        BlownupTrack.gameObject.transform.position = track;
    }
}
