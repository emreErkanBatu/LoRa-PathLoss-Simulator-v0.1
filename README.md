# LoRa-PathLoss-Simulator-v0.1

A configurable simulation environment for modeling LoRa RSSI behavior, path-loss characteristics, and obstacle-based attenuation under realistic conditions.  
This simulator is designed to support research on LoRa-based localization, signal propagation, and machine learning–driven performance prediction.

---
<p align="center">
  <a href="https://youtu.be/1tVO52E98Ys">
    <img src="https://img.youtube.com/vi/1tVO52E98Ys/maxresdefault.jpg" alt="LoRa Path-Loss Simulator v0.1 Demo" width="75%">
  </a>
</p>

## 🔍 Overview

`LoRa-PathLoss-Simulator-v0.1` provides a modular and extensible environment that models:

- Free-space path loss (FSPL)
- Obstacle-specific attenuation (wood, brick, glass, concrete, vegetation, etc.)
- Dynamic transmitter/receiver positions
- Mobile targets
- Environmental scenarios (Environment-1, Environment-2…)
- LoRa RSSI prediction
- Dataset generation for machine learning (e.g., MLP-based localization)

The simulator is suitable for:
- RSSI-based localization research  
- LoRa propagation studies  
- Machine learning training dataset creation  
- Academic experimentation and teaching  

---

##  Key Features

###  Obstacle Modeling
- Adjustable attenuation values per obstacle type  
- Multiple barrier layers and configurable material presets  
- Automatic cumulative attenuation calculation  

###  Signal Propagation Engine
- FSPL-based baseline model  
- Environment-dependent constants  
- Tunable noise and variability parameters  
- Realistic RSSI fluctuation modeling  

### Target Motion Simulation
- Static and dynamic node placement  
- Linear, random-walk, and custom trajectory support  
- Time-step-based simulation loop  

### Dataset Generation
- Exportable CSV dataset  
- Includes timestamp, node coordinates, target coordinates, FSPL, total attenuation, RSSI  
- Ready for MLP models  
