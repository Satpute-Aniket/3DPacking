# 3D Bin Packing Optimization Project
## Overview
This project addresses the 3D Container Loading Problem (CLP), a complex and computationally intensive task where the primary
objective is to optimize the packing of items into containers while minimizing overall logistics costs. The problem is NP-hard,
making it challenging to solve with exact methods alone, especially as the problem size increases. Our solution integrates both
exact and heuristic approaches to effectively manage and optimize this packing problem.

## Problem Statement

The project tackles three key aspects of the CLP:
1. Spatial Optimization:Efficiently arranging items within containers to maximize space utilization and ensure stable packing.
2. Feasibility of Transport: Ensuring that containers can be transported to their designated destinations without violating weight and volume constraints.
3. Cost Minimization: Reducing the overall costs associated with logistics, including transportation and storage, by optimizing the packing configuration.

## Methodology

### 1. Data Engineering & exploration
We began with comprehensive data engineering and exploration to understand the characteristics of the items to be packed. This step included analyzing item dimensions, weights, and other relevant features to inform our model development.

### 2. Mixed Integer Programming (MIP) model
We implemented a Mixed Integer Programming (MIP) model using Gurobi and Python. The MIP model is designed to optimize the assignment of items to containers, ensuring that:
- Every item gets packed only once.
- Weight and volume constraints are respected.
- The packing configuration minimizes the costs incurred.

### 3. Heuristic Method
We developed a Heuristic algorithm to arrange the items in the assigned container, to ensure speedy solution to the problem. The Heuristic algorithm tries to fit as many items assigned to the container as possible and rest of the items are marked as unpacked. 

![](https://github.com/Satpute-Aniket/3DPacking/blob/main/screenshots/Screenshot%202024-08-23%20235254.png)

### 4. Visualization and reporting
Data visualization techniques were used throughout the project to better understand the results and communicate findings. We presented the packing configurations and the performance of our model through clear and informative 3-Dimensional visualizations.
The visualisation showcases the container in question along with the orientation and position of the items placed in it.

![](https://github.com/Satpute-Aniket/3DPacking/blob/main/screenshots/Figure_1.png)

### 5. Results
The project achieved a packing efficiency of 95.62%, successfully processing 2,386 items into 135 containers (The containers are filled upto 90% of its volume). The total cost for this optimized packing solution was €6.33 million, showcasing significant cost savings through effective space utilization and strategic item placement. You can see the entire set of results in the below table:

| % Volume utilisation | Cost         | % change in cost | Packing efficiency (%) | Unpacked Items |
|:--------------------:|:------------:|:----------------:|:----------------------:|:--------------:|
| 100                  | 6.29 mn      | 0                | 91.07                  | 212            |
| 95                   | 6.31 mn      | 0.3              | 92.08                  | 188            |
| 90                   | 6.33 mn      | 0.6              | 95.62                  | 104            |
| 85                   | 6.37 mn      | 1.2              | 95.62                  | 104            |

These results were achieved in a runtime of just over an hour using a machine with a 8 core 16 threads AMD Rzyen 7 6800H CPU with 16GB of DDR5 RAM.

### 6. Tools and Technologies
- **Gurobi**: For solving the MIP model.
- **Python**: For data processing, model implementation, and heuristic methods.
- **mpl_toolkits & matplotlib**: To present the packing configurations and model performance clearly.

### 7. Conclusion
This project demonstrates a robust approach to solving the 3D Container Loading Problem by combining exact optimization methods with heuristic approaches. The solution effectively balances computational efficiency with practical application, delivering a cost-efficient and operationally feasible packing strategy.

### 8. Repository Structure
- **/Code**: Source code for the MIP model and heuristic methods along with notebooks for data exploration and model development.
- **/Resources**: All the research papers refered and used in the completion of this project.
- **/screenshots**: Screenshots used in this Readme.
- **MIP.pdf**: Mixed Integer Problem for the project
- **README.md**: Project overview and documentation.

> [!Note]
> The Input or the Output data cannot be made public as this project was carried out in collaboration with an organisation. We are thankfull for providing us with the problem statement and the required data.
