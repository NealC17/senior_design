import numpy as np 
from data_loader import bench, squat, deadlift
import pandas as pd 
from plotly.subplots import make_subplots
import plotly.graph_objects as go


def analyze_centered_signals(rep_df, title): 
    fig = go.Figure()
    print(rep_df[['gravityX', 'gravityY', 'gravityZ']])
    a = rep_df['gravityX']
    a -= np.mean(a)
    
    b = rep_df['gravityY'] 
    b -= np.mean(b)
    
    c = rep_df['gravityZ'] 
    c -= np.mean(c)
    
    fig.add_trace(
        go.Scatter(x=list(range(len(a))), y=a, name="gravityX")
    )
    fig.add_trace(
        go.Scatter(x=list(range(len(b))), y=b, name="gravityY")
    )
    fig.add_trace(
        go.Scatter(x=list(range(len(c))), y=c, name="gravityZ")
    )
    
    fig.update_layout(
        height=600, 
        title="Gravity Signals Over Time",
        xaxis_title="Time Steps",
        yaxis_title=title,
        hovermode="x unified", 
        legend=dict(
            title="Legend",  
            x=1,  
            y=1,  
            bordercolor="Black",  
            borderwidth=1  
        )
    )
    
    fig.show()

