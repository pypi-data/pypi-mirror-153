import plotly.graph_objects as go


def plot_curves(x, y, z, color: str = "black", width=2):
    return go.Scatter3d(x=x, y=y, z=z, mode='lines', line={"color": color, "width": width}, showlegend=False)


def plot_surf(x, y, z, w, cells, color="jet", opacity=1, flatshading=True):
    ijk = [[], [], []]
    for cell in cells:
        for idx in range(3):
            ijk[idx].append(cell[idx])
    fig = go.Mesh3d(x=x, y=y, z=z, i=ijk[0], j=ijk[1], k=ijk[2], colorscale=color, intensity=w, opacity=opacity,
                    flatshading=flatshading, showlegend=False)
    return fig


def plot_dist(x, y, z, w, color: str = "jet", size: int = 2, opacity: float = 1.):
    return go.Scatter3d(x=x, y=y, z=z, mode='markers', showlegend=False,
                        marker=dict(size=size, color=w, colorscale=color, opacity=opacity, showscale=True))


def plot_flux(x, y, z, u, v, w, size=1, color: str = "jet"):
    return go.Cone(x=x, y=y, z=z, u=u, v=v, w=w, colorscale=color, sizeref=size, showlegend=False)


def plot(*traces, camera=None, show_axes: bool = True, background_box=True):
    fig = go.Figure(layout=go.Layout(scene={'aspectmode': 'data'}))
    for trace in traces:
        fig.add_trace(trace)
    if camera is None:
        camera = {'eye': {'x': 1, 'y': -2, 'z': 1}}
    if not show_axes:
        fig.update_layout(
            scene=dict(
                xaxis=dict(title=' ', showticklabels=False),
                yaxis=dict(title=' ', showticklabels=False),
                zaxis=dict(title=' ', showticklabels=False),
            )
        )
    if not background_box:
        fig.update_layout(scene=dict(
            xaxis=dict(backgroundcolor="white"),
            yaxis=dict(backgroundcolor="white"),
            zaxis=dict(backgroundcolor="white"))
        )
    fig.update_layout(scene_camera=camera)
    return fig
