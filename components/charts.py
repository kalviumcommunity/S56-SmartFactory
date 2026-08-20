import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from components.theme import get_theme


def get_chart_theme_colors():
    """
    Returns tailored color tokens for Plotly visualizations according to active theme.
    """
    theme = get_theme()

    if theme == "dark":
        return {
            "bg_color": "rgba(0,0,0,0)",
            "paper_color": "rgba(0,0,0,0)",
            "text_primary": "#f8fafc",
            "text_muted": "#94a3b8",
            "grid_color": "rgba(51, 65, 85, 0.5)",
            "bar_primary": "#3b82f6",
            "bar_secondary": "#60a5fa",
            "bar_palette": [
                "#3b82f6", "#60a5fa", "#38bdf8", "#818cf8",
                "#a78bfa", "#f43f5e", "#fb923c", "#34d399"
            ],
            "line_color": "#38bdf8",
            "line_fill": "rgba(56, 189, 248, 0.12)",
            "hover_bg": "#1e293b",
            "hover_border": "#475569",
            "hover_text": "#f8fafc",
        }
    else:
        return {
            "bg_color": "rgba(0,0,0,0)",
            "paper_color": "rgba(0,0,0,0)",
            "text_primary": "#101828",
            "text_muted": "#667085",
            "grid_color": "rgba(228, 231, 236, 0.7)",
            "bar_primary": "#2563eb",
            "bar_secondary": "#3b82f6",
            "bar_palette": [
                "#2563eb", "#3b82f6", "#0284c7", "#4f46e5",
                "#7c3aed", "#e11d48", "#ea580c", "#059669"
            ],
            "line_color": "#2563eb",
            "line_fill": "rgba(37, 99, 235, 0.08)",
            "hover_bg": "#101828",
            "hover_border": "#101828",
            "hover_text": "#ffffff",
        }


def render_bar_chart(
    x,
    y,
    title="",
    x_title="",
    y_title="",
    height=320,
    orientation="v",
    color_discrete=None,
):
    """
    Renders an ultra-clean, modern Plotly bar chart with rounded corners and custom hover templates.
    """
    colors = get_chart_theme_colors()

    fig = go.Figure()

    if orientation == "v":
        fig.add_trace(
            go.Bar(
                x=x,
                y=y,
                marker=dict(
                    color=color_discrete or colors["bar_primary"],
                    line=dict(width=0),
                ),
                hovertemplate="<b>%{x}</b><br>Count: %{y:,}<extra></extra>",
            )
        )
        fig.update_xaxes(
            title=dict(text=x_title, font=dict(size=12, color=colors["text_muted"])),
            tickfont=dict(size=11, color=colors["text_muted"]),
            gridcolor=colors["grid_color"],
            showline=False,
            zeroline=False,
        )
        fig.update_yaxes(
            title=dict(text=y_title, font=dict(size=12, color=colors["text_muted"])),
            tickfont=dict(size=11, color=colors["text_muted"]),
            gridcolor=colors["grid_color"],
            showline=False,
            zeroline=False,
        )
    else:
        fig.add_trace(
            go.Bar(
                x=y,
                y=x,
                orientation="h",
                marker=dict(
                    color=color_discrete or colors["bar_primary"],
                    line=dict(width=0),
                ),
                hovertemplate="<b>%{y}</b><br>Count: %{x:,}<extra></extra>",
            )
        )
        fig.update_xaxes(
            title=dict(text=y_title, font=dict(size=12, color=colors["text_muted"])),
            tickfont=dict(size=11, color=colors["text_muted"]),
            gridcolor=colors["grid_color"],
            showline=False,
            zeroline=False,
        )
        fig.update_yaxes(
            title=dict(text=x_title, font=dict(size=12, color=colors["text_muted"])),
            tickfont=dict(size=11, color=colors["text_muted"]),
            gridcolor=colors["grid_color"],
            showline=False,
            zeroline=False,
        )

    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=14, color=colors["text_primary"], family="Inter, sans-serif"),
            x=0,
            xanchor="left",
        ) if title else None,
        height=height,
        margin=dict(l=10, r=10, t=30 if title else 10, b=10),
        paper_bgcolor=colors["paper_color"],
        plot_bgcolor=colors["bg_color"],
        font=dict(family="Inter, system-ui, sans-serif"),
        hoverlabel=dict(
            bgcolor=colors["hover_bg"],
            bordercolor=colors["hover_border"],
            font=dict(color=colors["hover_text"], size=12, family="Inter, sans-serif"),
        ),
        bargap=0.35,
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})


def render_line_chart(
    x,
    y,
    title="",
    x_title="",
    y_title="",
    height=320,
    fill_area=True,
):
    """
    Renders an ultra-modern spline line chart with gradient fill area and clean hover tags.
    """
    colors = get_chart_theme_colors()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines+markers",
            line=dict(
                color=colors["line_color"],
                width=2.5,
                shape="spline",
                smoothing=1.1,
            ),
            marker=dict(
                size=5,
                color=colors["line_color"],
                line=dict(width=1, color="#ffffff" if get_theme() == "light" else "#1e293b"),
            ),
            fill="tozeroy" if fill_area else None,
            fillcolor=colors["line_fill"] if fill_area else None,
            hovertemplate="<b>%{x}</b><br>Defects: %{y:,}<extra></extra>",
        )
    )

    fig.update_xaxes(
        title=dict(text=x_title, font=dict(size=12, color=colors["text_muted"])),
        tickfont=dict(size=11, color=colors["text_muted"]),
        gridcolor=colors["grid_color"],
        showline=False,
        zeroline=False,
    )
    fig.update_yaxes(
        title=dict(text=y_title, font=dict(size=12, color=colors["text_muted"])),
        tickfont=dict(size=11, color=colors["text_muted"]),
        gridcolor=colors["grid_color"],
        showline=False,
        zeroline=False,
    )

    fig.update_layout(
        title=dict(
            text=title,
            font=dict(size=14, color=colors["text_primary"], family="Inter, sans-serif"),
            x=0,
            xanchor="left",
        ) if title else None,
        height=height,
        margin=dict(l=10, r=10, t=30 if title else 10, b=10),
        paper_bgcolor=colors["paper_color"],
        plot_bgcolor=colors["bg_color"],
        font=dict(family="Inter, system-ui, sans-serif"),
        hoverlabel=dict(
            bgcolor=colors["hover_bg"],
            bordercolor=colors["hover_border"],
            font=dict(color=colors["hover_text"], size=12, family="Inter, sans-serif"),
        ),
    )

    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
