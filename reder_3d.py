
file_path = r"samples\centipede.stl"
if st.sidebar.button("render model"):

    ## Initialize a plotter object
    plotter = pv.Plotter(window_size=[400,400])

    ## Load the mesh from file
    mesh = pv.read(file_path)


    ## Add mesh to the plotter
    plotter.add_mesh(mesh, cmap='bwr')

    ## Final touches
    plotter.view_isometric()
    plotter.background_color = 'white'

    ## Send to streamlit
    stpyvista(plotter, key="pv_cube")
