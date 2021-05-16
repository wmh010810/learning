import vtk
import time
import serial

cone = vtk.vtkConeSource()

mapper = vtk.vtkPolyDataMapper()
mapper.SetInputConnection(cone.GetOutputPort())

actor = vtk.vtkActor()
actor.SetMapper(mapper)

# create coordinate axes in the render window
axes = vtk.vtkAxesActor()
axes.SetTotalLength(10, 20, 30)
axes.SetShaftType(0)
axes.SetAxisLabels(0)
axes.SetCylinderRadius(0.02)

filename = "arm.stl"

reader = vtk.vtkSTLReader()
reader.SetFileName(filename)

mapper1 = vtk.vtkPolyDataMapper()
mapper1.SetInputConnection(reader.GetOutputPort())

actor1 = vtk.vtkActor()
actor1.SetMapper(mapper1)

window = vtk.vtkRenderWindow()  # Sets the pixel width, length of the window.
window.SetSize(500, 500)

interactor = vtk.vtkRenderWindowInteractor()
interactor.SetRenderWindow(window)

renderer = vtk.vtkRenderer()
window.AddRenderer(renderer)

renderer.AddActor(actor)
renderer.AddActor(actor1)
renderer.AddActor(axes)
renderer.SetBackground(0, 0, 1)

actor.SetOrigin(0.5, 0, 0)
print("bbbbbbbbbbbbbbbbbbbbbbbbbbb", actor1.GetBounds())
print("CCCCCCCCCCCCCCCCCCCCC", actor1.GetCenter())
actor1.SetOrigin(-16, 48, 122)
actor1.SetPosition(16, -48, -122)
actor1.SetScale(0.1, 0.1, 0.1)

for i in range(36):
    time.sleep(0.1)
    actor.RotateX(10)
    print(actor.GetOrientation())
    actor.SetOrientation(0, i * 30, 0)
    actor.AddOrientation(5, 0, 0)
    actor1.RotateX(10)
    window.Render()

ser = serial.Serial("COM21", timeout=0.1)

while True:
    print("reading....")
    resp = ser.readline()
    if resp != b"":
        a = resp.decode()
        print(a)
        print("get commnd, I will handle it", resp)
        b = a.strip()
        if b == '~':
            break
        c = b.split(",")
        d = list(map(int, c))
        servo1 = d[0]
        servo2 = d[1]
        servo3 = d[2]
        print("move servo to angle", servo1, servo2, servo3)
        actor1.SetOrientation(servo1, 0, 0)
    else:
        print("working on something else..")
    window.Render()

interactor.Start()
