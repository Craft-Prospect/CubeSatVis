#!/usr/bin/env python

"""Visualisation.py: Visualise data from simulation"""

__author__ = "Murray Ireland"
__email__ = "murray@craftprospect.com"
__date__ = "22/10/2018"
__copyright__ = "Copyright 2017 Craft Prospect Ltd"
__licence___ = ""

import vtk
import numpy as np
from math import tan, sin, cos, atan, pi
# import msvcrt
import sys, os
import platform
from datetime import datetime
from time import sleep

if platform.system() == "Windows":
    from win32api import GetSystemMetrics
    screen_size = (GetSystemMetrics(0), GetSystemMetrics(1))
elif platform.system() == "Linux":
    try:
        import tkinter as tk
    except ImportError:
        import Tkinter as tk

    root = tk.Tk()
    screen_size = (root.winfo_screenwidth(), root.winfo_screenheight())

# Get current and base directories
cur_dir = os.path.dirname(os.path.realpath(__file__))
if "\\" in cur_dir:
    base_dir = "/".join(cur_dir.split("\\"))
else:
    base_dir = cur_dir

class Visualisation(object):
    """Class for visualisation object"""

    # Scale time
    TIME_SCALE = 1

    # Turn text overlay on/off
    SHOW_TEXT = True

    # Full-screen and window scaling
    FULL_SCREEN = True
    WIN_H_SCALE = 1.
    WIN_V_SCALE = 1.
    TEXT_SCALE = 1.

    # Use lower resolution textures where appropriate
    USE_SMALL_IMAGES = False

    # Scale entire animation for troubleshooting
    ANI_SCALE = 1.

    # Scale satellite up for better visibility
    SAT_SCALE = 500.   # Breaks if too small

    # Colours
    COLOUR_BG = (0, 0, 0)
    COLOUR_FONT = (0.871, 0.246, 0.246)

    # Set solar panel angles [deg]
    PANEL_ANGLE = 10

    # Tile size for Earth textures [m]
    TILE_SIZE = (177390, 183360)

    # Anchor settings
    ANCHOR = {
        "SW": (0, 0),
        "NW": (0, 2),
        "NE": (2, 2),
        "SE": (2, 0),
        "N": (1, 2),
        "E": (2, 1),
        "S": (1, 0),
        "W": (0, 1),
        "C": (1, 1)
    }

    def __init__(self, PROPS, data):
        """Class constructor"""

        # Screen size and aspect ratio
        self.SCREEN_SIZE = (screen_size[0], screen_size[1])
        self.SCREEN_AR = float(self.SCREEN_SIZE[0])/float(self.SCREEN_SIZE[1])

        # Initialise property dictionaries
        self.SAT_PROPS = PROPS["Sat"]
        self.CAM_PROPS = PROPS["Camera"]
        self.IMG_PROPS = PROPS["Imagery"]
        self.LSR_POS = PROPS["Laser"]
        self.EARTH_PROPS = PROPS["Earth"]

        # Initialise simulation data
        self.DATA = data

        # Initialise imagery
        self.IMG_PROPS["Texture size"] = (
            self.IMG_PROPS["Size"]["full"][0]*self.IMG_PROPS["Res"]["full"],
            self.IMG_PROPS["Size"]["full"][1]*self.IMG_PROPS["Res"]["full"]
        )

        # Initialise index
        self.index = 0

        # Initialise render window and interactor
        self.renWin, self.iren = self.init_renderer()
        self.ren = {}

        # Create scenes
        self.actors, self.cameras, self.text, self.lights = self.create_scenes()

        for key in self.lights.keys():
            for light in self.lights[key]:
                self.ren[key].AddLight(light)

        # Render scenes
        self.iren.Initialize()
        self.renWin.Render()
        
        # Initialise time
        now = datetime.now()
        self.init_time = [now.hour, now.minute, now.second]

        # Create timer event
        self.iren.AddObserver("TimerEvent", self.execute)
        timerId = self.iren.CreateRepeatingTimer(int(1000*self.DATA["Time step"]))

        # Start interactor and timer
        self.iren.Start()

        # Stop timer?
        # self.movieWriter.End()

    def init_renderer(self):
        """Initialise render window and interactor"""

        # Initialise render window
        renWin = vtk.vtkRenderWindow()
        if self.FULL_SCREEN:
            renWin.FullScreenOn()
        else:
            renWin.SetSize(
                int(self.WIN_H_SCALE*self.SCREEN_SIZE[0]),
                int(self.WIN_V_SCALE*self.SCREEN_SIZE[1])
            )

        class MyInteractorStyle(vtk.vtkInteractorStyleTrackballCamera):

            def __init__(self, parent=None):
                return None

        # Initialise interactor
        iren = vtk.vtkRenderWindowInteractor()
        iren.SetInteractorStyle(MyInteractorStyle())
        # iren.AutoAdjustCameraClippingRangeOn()
        iren.SetRenderWindow(renWin)

        return renWin, iren

    def init_video(self):
        """Initialise video recorder"""

        # Set up filter
        imageFilter = vtk.vtkWindowToImageFilter()
        imageFilter.SetInput(self.renWin)
        imageFilter.SetInputBufferTypeToRGB()
        imageFilter.ReadFrontBufferOff()
        imageFilter.Update()

        return imageFilter, 0

    def add_to_ren(self, name, actors, camera, viewport, text):
        """Add elements of scene to renderer window"""

        # Create renderer for scene
        self.ren[name] = vtk.vtkRenderer()

        # Add renderer to render window
        self.renWin.AddRenderer(self.ren[name])

        # Add camera and viewport
        if camera != []:
            self.ren[name].SetActiveCamera(camera)
        self.ren[name].SetViewport(viewport)

        # Add actors
        for key in actors:
            if type(actors[key]) is list:
                for actor in actors[key]:
                    self.ren[name].AddActor(actor)
            else:
                self.ren[name].AddActor(actors[key])

        self.ren[name].ResetCameraClippingRange()

        # Add text
        if type(text) is dict:
            for actor in text:
                self.ren[name].AddActor(text[actor])
        else:
            self.ren[name].AddActor(text)

        self.ren[name].SetBackground(self.COLOUR_BG)

    def create_scenes(self):
        """Create scenes"""

        # Initialise dictionaries
        cameras = {}
        text = {}
        lights = {}

        # Create scenes
        actors, cameras["Main"], text["Main"], lights["Main"] = self.scene_main()

        # Return actors and cameras
        return actors, cameras, text, lights

    def scene_main(self):
        """Create main scene"""

        # Create viewport
        viewport = [0, 0, 1, 1]

        # Camera settings

        # Focal point offset from sat centre
        foffset = [200, -400, 0]

        # Distance from sat
        cam_dist = 5e3

        # Angles
        pitch = -65
        yaw = 2
        
        # Focal point
        fpoint = np.array([0., 0., -self.SAT_PROPS["Alt"]]) + np.array(foffset)

        # Transform camera position
        prad = pitch*pi/180
        yrad = yaw*pi/180
        Rpitch = np.matrix([
            [cos(prad), 0, sin(prad)],
            [0, 1, 0],
            [-sin(prad), 0, cos(prad)]
        ])
        Ryaw = np.matrix([
            [cos(yrad), -sin(yrad), 0],
            [sin(yrad), cos(yrad), 0],
            [0, 0, 1]
        ])

        cam_pos = Ryaw*Rpitch*np.matrix([-cam_dist, 0., 0.]).T
        cam_pos = np.array(cam_pos).flatten()
        cam_pos = cam_pos + fpoint

        # cam_pos = [-10, 0., -self.SAT_PROPS["Alt"] - cam_dist]

        # Create camera
        camera = vtk.vtkCamera()
        camera.SetPosition(cam_pos)
        camera.SetViewUp(0, 0, -1)
        camera.SetViewAngle(15)
        camera.SetFocalPoint(fpoint)
        camera.SetClippingRange(0.001, 100)

        # Create lights
        lights = []
        lights.append(vtk.vtkLight())
        lights[0].SetPosition(cam_pos)
        lights[0].SetFocalPoint([0., 0., -self.SAT_PROPS["Alt"]])
        lights[0].SetColor(1., 1., 1.)
        lights.append(vtk.vtkLight())
        lights[1].SetPosition(0., 0., 0)
        lights[1].SetFocalPoint([0., 0., -self.SAT_PROPS["Alt"]])

        # Create actors
        actors = {
            "Sat body": self.create_sat_body(),
            "Sat panels": self.create_sat_panels(),
            "Earth": self.create_earth("true", "small"),
            "Forward cam": self.create_cam_fov("Forward"),
            "Redline": self.create_line(self.LSR_POS["Red"], [1., 0., 0.]),
            "Greenline": self.create_line(self.LSR_POS["Green"], [0., 1., 0.]),
            "Blueline": self.create_line(self.LSR_POS["Blue"], [0., 0., 1.])
        }

        for T, pos in zip(range(self.DATA["Target info"]["Num"]), self.DATA["Target info"]["Pos"]):
            actors["T{}".format(T+1)] = self.create_sphere(pos)

        # Text actors
        text = {}

        if self.SHOW_TEXT:
            # Craft text
            text["Craft"] = self.create_text(
                {
                    "String": "CRAFT PROSPECT",
                    "Size": 60,
                    "Font": "Montserrat-SemiBold",
                    "Y offset": 0.06
                },
                viewport
            )

            # Subtitle text
            text["QKD"] = self.create_text(
                {
                    "String": "Demo Simulation",
                    "Size": 40,
                    "Style": "Normal"
                },
                viewport
            )

            # Time text
            text["Time"] = self.create_text(
                {
                    "String": "",
                    "Size": 50,
                    "Anchor": "NE",
                    "Font": "7Segment"
                },
                viewport
            )

            # Info text
            text["Info"] = self.create_text(
                {
                    "String": """Altitude: {:.0f} km
                    Velocity: {:.2f} km/s
                    """.format(
                        self.SAT_PROPS["Alt"]/1000,
                        self.DATA["Vel"][0, 0]/1000,
                    ),
                    "Size": 20,
                    "Anchor": "NE",
                    "Y offset": 0.06
                },
                viewport
            )

        # Render scene
        self.add_to_ren("Main", actors, camera, viewport, text)

        # Reset clipping range
        # camera.SetClippingRange(1000, 1000e3)

        # Return actors to animate
        return actors, camera, text, lights

    def create_sat_body(self):
        """Generate satellite body geometry"""

        # Dimensions of body
        SAT_SIZE = self.ANI_SCALE*self.SAT_SCALE*np.asarray(self.SAT_PROPS["Size"])/2
        bx = SAT_SIZE[0]
        by = SAT_SIZE[1]
        bz = SAT_SIZE[2]

        # Create vertices in body frame
        ind = 0
        V = []
        for x in [-1, 1]:
            for y in [-1, 1]:
                for z in [-1, 1]:
                    V.append((bx*x, by*y, bz*z))
        
        # Create faces
        F = [
            (0, 1, 3, 2),
            (4, 5, 7, 6),
            (0, 1, 5, 4),
            (2, 3, 7, 6),
            (0, 2, 6, 4),
            (1, 3, 7, 5)
        ]

        # Create building blocks of polydata
        sat = vtk.vtkPolyData()
        points = vtk.vtkPoints()
        polys = vtk.vtkCellArray()
        scalars = vtk.vtkFloatArray()

        # Load the point, cell and data attributes
        for i in range(len(V)):
            points.InsertPoint(i, V[i])
        for i in range(len(F)):
            polys.InsertNextCell(self.mkVtkIdList(F[i]))
        for i in range(len(V)):
            scalars.InsertTuple1(i, i)
        
        # Assign the pieces to the vtkPolyData.
        sat.SetPoints(points)
        del points
        sat.SetPolys(polys)
        del polys
        sat.GetPointData().SetScalars(scalars)
        del scalars

        # Mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(sat)
        mapper.ScalarVisibilityOff()

        # Actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(0.5, 0.5, 0.5)
        actor.GetProperty().SetAmbient(0.5)
        actor.GetProperty().SetSpecular(1.0)
        actor.GetProperty().SetSpecularPower(5.0)
        actor.GetProperty().SetDiffuse(0.2)

        # Move to sat position
        actor.SetPosition(0, 0, -self.SAT_PROPS["Alt"])

        return actor

    def create_sat_panels(self):
        """Create satellite solar panel geometry"""

        # Dimensions of body
        SAT_SIZE = self.ANI_SCALE*self.SAT_SCALE*np.asarray(self.SAT_PROPS["Size"])/2
        bx = SAT_SIZE[0]
        by = SAT_SIZE[1]
        bz = SAT_SIZE[2]

        # Panel length
        L = bx

        # Panels
        theta = self.PANEL_ANGLE*pi/180
        px1 = bx - L*sin(theta)
        py1 = by + L*cos(theta)
        pz1 = bz
        px2 = px1 + L*sin(theta)
        py2 = py1 + L*cos(theta)
        pz2 = pz1

        # Vertices
        V = [
            (-bx, by, -bz),
            (-bx, by, bz),
            (-px1, py1, pz1),
            (-px1, py1, -pz1),
            (-px1, py1, -pz1),
            (-px1, py1, pz1),
            (-px2, py2, pz2),
            (-px2, py2, -pz2),
            (-bx, -by, -bz),
            (-bx, -by, bz),
            (-px1, -py1, pz1),
            (-px1, -py1, -pz1),
            (-px1, -py1, -pz1),
            (-px1, -py1, pz1),
            (-px2, -py2, pz2),
            (-px2, -py2, -pz2)
        ]

        # Create faces
        F = [
            (0, 1, 2, 3),
            (4, 5, 6, 7),
            (8, 9, 10, 11),
            (12, 13, 14, 15)
        ]

        # Create building blocks of polydata
        sat = vtk.vtkPolyData()
        points = vtk.vtkPoints()
        polys = vtk.vtkCellArray()
        scalars = vtk.vtkFloatArray()

        # Load the point, cell and data attributes
        for i in range(len(V)):
            points.InsertPoint(i, V[i])
        for i in range(len(F)):
            polys.InsertNextCell(self.mkVtkIdList(F[i]))
        for i in range(len(V)):
            scalars.InsertTuple1(i, i)
        
        # Assign the pieces to the vtkPolyData.
        sat.SetPoints(points)
        del points
        sat.SetPolys(polys)
        del polys
        sat.GetPointData().SetScalars(scalars)
        del scalars

        # Mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(sat)
        mapper.ScalarVisibilityOff()

        # Actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(0., 0., 0.8)
        actor.GetProperty().SetAmbient(0.5)
        actor.GetProperty().SetSpecular(.5)
        actor.GetProperty().SetSpecularPower(10.0)
        actor.GetProperty().SetDiffuse(0.2)

        # Move to sat position
        actor.SetPosition(0, 0, -self.SAT_PROPS["Alt"])

        return actor

    def create_earth(self, imtype, size):
        """Create tiles for Earth geometry"""

        # Update properties for tile
        tile_props = {
            "Size": self.IMG_PROPS["Texture size"],
            "Translate": (
                -self.IMG_PROPS["Offset"][0],
                -self.IMG_PROPS["Texture size"][1]/2,
                0
            )
        }

        # Texture for tile
        texture = f"{cur_dir}/images/samp1_{size}.jpg"

        # Create actors
        actor = self.create_plane(tile_props, texture)

        return actor

    def create_plane(self, props, texture):
        """Create flat plane"""

        # Pull and scale dimensions
        SIZE = np.asarray(props["Size"])
        POS = np.asarray(props["Translate"])

        # Create texture reader
        reader = vtk.vtkJPEGReader()
        reader.SetFileName(texture)

        # Create texture object
        texture = vtk.vtkTexture()
        texture.SetInputConnection(reader.GetOutputPort())
        texture.InterpolateOn()

        # Create plane model
        plane = vtk.vtkPlaneSource()
        plane.SetResolution(1, 1)
        plane.SetPoint1(0, SIZE[1], 0)
        plane.SetPoint2(SIZE[0], 0, 0)

        # Translate to centre
        transP = vtk.vtkTransform()
        transP.Translate(
            POS[0],
            POS[1],
            POS[2]
        )
        tpd = vtk.vtkTransformPolyDataFilter()
        tpd.SetInputConnection(plane.GetOutputPort())
        tpd.SetTransform(transP)
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(tpd.GetOutputPort())
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.SetTexture(texture)
        actor.GetProperty().SetAmbient(1.0)
        actor.GetProperty().SetSpecular(.5)
        actor.GetProperty().SetSpecularPower(5.0)
        actor.GetProperty().SetDiffuse(0.2)

        return actor

    def create_cam_fov(self, name):
        """Create FOV actor for camera"""

        # Vertices of FOV
        V = [
            (0, 0, -self.SAT_PROPS["Alt"]),
            tuple(self.CAM_PROPS[name]["Intercepts"][:, 0]),
            tuple(self.CAM_PROPS[name]["Intercepts"][:, 1]),
            tuple(self.CAM_PROPS[name]["Intercepts"][:, 2]),
            tuple(self.CAM_PROPS[name]["Intercepts"][:, 3])
        ]

        # Faces of FOV
        F = [(0, 1, 2), (0, 2, 3), (0, 3, 4), (0, 4, 1)]

        # Create building blocks of polydata
        cam = vtk.vtkPolyData()
        points = vtk.vtkPoints()
        polys = vtk.vtkCellArray()
        scalars = vtk.vtkFloatArray()

        # Load the point, cell and data attributes
        for i in range(5):
            points.InsertPoint(i, V[i])
        for i in range(4):
            polys.InsertNextCell( self.mkVtkIdList(F[i]))
        for i in range(5):
            scalars.InsertTuple1(i,i)

        # Assign the pieces to the vtkPolyData.
        cam.SetPoints(points)
        del points
        cam.SetPolys(polys)
        del polys
        cam.GetPointData().SetScalars(scalars)
        del scalars

        # Mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputData(cam)
        mapper.ScalarVisibilityOff()

        # Actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(0.5, 1, 0.5)
        actor.GetProperty().SetAmbient(0.5)
        actor.GetProperty().SetOpacity(0.1)

        return actor

    def create_line(self, pos, colour):
        """Create line"""

        # Absolute source position
        pos_abs = np.array([0., 0., -self.SAT_PROPS["Alt"]]) + np.array(pos)*self.SAT_SCALE

        # Create line
        line = vtk.vtkLineSource()
        line.SetPoint1(pos_abs)
        line.SetPoint2(2*self.SAT_PROPS["Alt"], 0., -self.SAT_PROPS["Alt"])
        
        # Mapper
        mapper = vtk.vtkPolyDataMapper()
        mapper.SetInputConnection(line.GetOutputPort())
        
        # Actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(colour)
        actor.GetProperty().SetOpacity(0.5)
        actor.GetProperty().SetLineWidth(4)
        actor.SetOrigin(0., 0., -self.SAT_PROPS["Alt"])

        return actor

    def create_sphere(self, position):
        """Create sphere of specific size"""

        # Create source
        source = vtk.vtkSphereSource()
        source.SetCenter(0, 0, 0)
        source.SetRadius(1.e3)
        source.SetPhiResolution(40)
        source.SetThetaResolution(40)

        # Mapper
        mapper = vtk.vtkPolyDataMapper()
        if vtk.VTK_MAJOR_VERSION <= 5:
            mapper.SetInput(source.GetOutput())
        else:
            mapper.SetInputConnection(source.GetOutputPort())

        # Actor
        actor = vtk.vtkActor()
        actor.SetMapper(mapper)
        actor.GetProperty().SetColor(1, 0.5, 0.5)
        actor.GetProperty().SetAmbient(0.5)
        actor.GetProperty().SetOpacity(0.8)
        actor.SetPosition(position)

        # Return actor
        return actor
    
    def create_text(self, settings, viewport):
        """Create text actor for view labels"""

        viewport = np.array(viewport)
        viewport[[0, 2]] = self.WIN_H_SCALE*viewport[[0, 2]]
        viewport[[1, 3]] = self.WIN_V_SCALE*viewport[[1, 3]]
        viewport = list(viewport)

        # Set defaults if not specified
        defaults = {
            "Size": 20,
            "Anchor": "SW",
            "X offset": 0.02,
            "Y offset": 0.02,
            "Font": "Montserrat",
            "Colour": self.COLOUR_FONT
        }
        for key in defaults:
            try:
                settings[key]
            except KeyError:
                settings[key] = defaults[key]

        # Position
        margin = (
            self.TEXT_SCALE*settings["X offset"]*(self.ANCHOR[settings["Anchor"]][0] - 1),
            self.TEXT_SCALE*settings["Y offset"]*(self.ANCHOR[settings["Anchor"]][1] - 1)
        )

        posx = int((viewport[0] + 0.5*self.ANCHOR[settings["Anchor"]][0]*(viewport[2] - viewport[0]) - margin[0])*self.SCREEN_SIZE[0])
        posy = int((viewport[1] + 0.5*self.ANCHOR[settings["Anchor"]][1]*(viewport[3] - viewport[1]) - margin[1])*self.SCREEN_SIZE[1])

        # Properties
        props = vtk.vtkTextProperty()
        props.SetFontFamily(vtk.VTK_FONT_FILE)
        if settings["Font"] == "Montserrat-SemiBold":
            props.SetFontFile("./fonts/Montserrat-SemiBold.ttf")
        elif settings["Font"] == "Consolas":
            props.SetFontFile("./fonts/consola.ttf")
        elif settings["Font"] is "7Segment":
            props.SetFontFile("./fonts/digital-7 (mono).ttf")
        else:
            props.SetFontFile("./fonts/Montserrat.ttf")
        
        props.SetFontSize(int(self.TEXT_SCALE*settings["Size"]))
        props.SetColor(settings["Colour"])
        props.SetJustification(self.ANCHOR[settings["Anchor"]][0])
        props.SetVerticalJustification(self.ANCHOR[settings["Anchor"]][1])

        # Create actor
        actor = vtk.vtkTextActor()
        actor.SetInput(settings["String"])
        actor.SetDisplayPosition(posx, posy)
        actor.SetTextProperty(props)

        return actor

    def execute(self, obj, event):
        """Execute timed event"""

        # Reset clipping range
        # self.cameras["Main"].SetClippingRange(1000, 3000e3)

        # Simulation time
        T = self.DATA["Time"][self.index]

        # Visualisation time
        Tvis = T*self.TIME_SCALE

        # Modes
        adcs_mode = self.DATA["ADCS mode names"][int(self.DATA["ADCS mode"][self.index])]
        payload_mode = self.DATA["Payload mode names"][int(self.DATA["Payload mode"][self.index])]

        # Update Earth position
        self.actors["Earth"].SetPosition(
            -self.DATA["Pos"][0, self.index],
            0,
            0
        )

        # Update target positions
        for trgt, pos in zip(range(self.DATA["Target info"]["Num"]), self.DATA["Target info"]["Pos"]):
            self.actors["T{}".format(trgt+1)].SetPosition(
                -self.DATA["Pos"][0, self.index] + pos[0],
                pos[1],
                pos[2]
            )

        # Update sightline
        att_des = tuple(np.array(self.DATA["Inputs"][:, self.index])*180/pi)
        self.actors["Redline"].SetOrientation(att_des)
        self.actors["Greenline"].SetOrientation(att_des)
        self.actors["Blueline"].SetOrientation(att_des)

        if payload_mode in ["Synchronise"]:
            self.actors["Redline"].GetProperty().SetOpacity(0)
            self.actors["Greenline"].GetProperty().SetOpacity(0.9)
            self.actors["Blueline"].GetProperty().SetOpacity(0)
        elif payload_mode in ["Authenticate"]:
            self.actors["Redline"].GetProperty().SetOpacity(0)
            self.actors["Greenline"].GetProperty().SetOpacity(0)
            self.actors["Blueline"].GetProperty().SetOpacity(0.9)
        elif payload_mode in ["Key delivery"]:
            self.actors["Redline"].GetProperty().SetOpacity(0.9)
            self.actors["Greenline"].GetProperty().SetOpacity(0)
            self.actors["Blueline"].GetProperty().SetOpacity(0.9)
        else:
            self.actors["Redline"].GetProperty().SetOpacity(0)
            self.actors["Greenline"].GetProperty().SetOpacity(0)
            self.actors["Blueline"].GetProperty().SetOpacity(0)

        # Update satellite attitude
        att = tuple(np.array(self.DATA["Att"][:, self.index])*180/pi)
        for key in ["Sat body", "Sat panels"]:
            self.actors[key].SetOrientation(att)

        # Update text actors
        hh = self.init_time[0]
        ss = int(self.init_time[2] + Tvis)
        mm = self.init_time[1] + (ss // 60)
        ss =  ss % 60
        hh = hh + (mm // 60)
        mm = mm % 60
        self.text["Main"]["Time"].SetInput(
            "{:02d}:{:02d}:{:02d}".format(hh, mm, ss)
        )
        # Update render window interactor
        self.iren = obj
        self.iren.GetRenderWindow().Render()

        # Increment index, loop if at end of data
        if self.index < len(self.DATA["Time"]) - 1:
            self.index += 1
        else:
            self.index = 0

    def mkVtkIdList(self, it):
        """Makes a vtkIdList from a Python iterable"""
        vil = vtk.vtkIdList()
        for i in it:
            vil.InsertNextId(int(i))
        return vil


