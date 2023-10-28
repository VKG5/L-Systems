# L-Systems
This is an add-on for Lindenmayer systems within Blender. The add-on creates fractal patterns (Currently limited to 2D patterns) within Blender. It uses the Blender Python API to do so and supports a limited grammar as of the moment. 

## User Interface
<!-- Adding an image -->
<p align="center">
  <img src="/Images/L-System%231.png" width="512" title="User Interface"> 
</p>

The user interface provides simple to understand, self-explanatory briefs about how to use the tool. The list of supported grammar is given below:
- [x] F/G : Go forward by some number of units
- [ ] B : Go backward by some number of units
- [x] X : Doesn't do anything, acts as a placeholder
- [x] - : Turn left by some degrees
- [x] + : Turn right by some degrees
- [x] [ : Corresponds to saving the current values for position and angle
- [x] ] : Executing the saved values in '['

*(We turn 60 degrees by default)*

## Samples
<!-- Adding an image -->
<p align="center">
  <img src="/Images/L-System%232.png" width="512" title="Samples"> 
</p>

There are a bunch of sample curves/systems that can be generated. These should help you get started with the tool and give you a basic idea about the working. For further details and study, please refer to [learn](https://en.wikipedia.org/wiki/L-system). A few eamples of generated patterns can be found down below.

## Samples
<!-- Adding an image -->
<p align="center">
  <img src="/Images/KochCurve.png" width="512" title="A Koch Curve"> 
  <img src="/Images/KochSnowflake.png" width="512" title="Snowflake"> 
  <img src="/Images/DragonCurve.png" width="512" title="A curve representing a dragon"> 
  <img src="/Images/FractalPlant.png" width="512" title="Fractal Plant - 2D Tree/Fern"> 
</p>

## Code
The whole tool has been written in Python, on the Blender Python API. There are no extra dependencies and this should work with all 3.2.0+ builds of Blender. The code is heavily commented and modular. Please feel free to have a look!

<!-- Adding an image -->
<p align="center">
  <img src="/Images/Code.png" width="512" title="Sample Code = Comments and Modular (Funtions)"> 
</p>

## Demo Video:
[<img src="https://img.youtube.com/vi/1C7roLeTzXY/hqdefault.jpg" height="300"/>](https://www.youtube.com/embed/1C7roLeTzXY)

### NOTE : THIS IS STILL A WIP. You are free to make changes and use it as and when necessary. Don't forget to give credits where necessary!
