# -*- coding: utf-8 -*-
"""
Created on Fri Jan 28 22:24:41 2022

@author: Yates


"""


def quit_project(mws):
    mws.Quit()

def save_project(mws):
    mws.Save()
    
def save_as_project(mws, filename):
    mws.SaveAs(f'{filename}.cst')

def save_zip(mws, keepAll, keep1D, keepFarfield, deleteProjFolder):
    mws.StoreinArchive(keepAll, keep1D, keepFarfield, deleteProjFolder)
    
def backup(mws, filename):
    mws.Backup(f'{filename}.cst')
    

    
# intialise default units 
def default_units(mws):
    units = mws.Units
    units.Geometry("mm")
    units.Frequency("GHz")
    units.TemperatureUnit("Kelvin")
    units.Time("ns")
    units.Voltage("V")
    units.Current("A")
    units.Resistance("Ohm")
    units.Conductance("Siemens")
    units.Capacitance("PikoF")
    units.Inductance("NanoH")
    

def activate_local_wcs(mws, setNormal, setOrigin, setUVector, activate):
    wcs = mws.WCS

    if activate:
        wcs.activateWCS('local')
        wcs.setNormal(str(setNormal(0)), str(setNormal(1)), str(setNormal(2)))
        wcs.setOrigin(str(setOrigin(0)), str(setOrigin(1)), str(setOrigin(2)))
        wcs.setUVector(str(setUVector(0)), str(setUVector(1)), str(setUVector(2)))
    else:
        wcs.ActivateWCS('Global')
    
def mesh_initiator(mws):
    FDSolver = mws.FDSolver
    mesh = mws.Mesh
    mesh_settings = mws.MeshSettings
    meshAdaption3D = mws.MeshAdaption3D
    PostProcess1D = mws.PostProcess1D

    FDSolver.ExtrudeOpenBC('True')

    mesh.MergeThinPECLayerFixpoints('True')
    mesh.RatioLimit('20')
    mesh.AutomeshRefineAtPecLines('True', '6')
    mesh.FPBAAvoidNonRegUnite('True')
    mesh.ConsiderSpaceForLowerMeshLimit('False')
    mesh.MinimumStepNumber('5')
    mesh.AnisotropicCurvatureRefinement('True')
    mesh.AnisotropicCurvatureRefinementFSM('True')
    
    # Defualt mesh settings 
    
    mesh_settings.SetMeshType('Hex')
    mesh_settings.Set('RatioLimitGeometry', '20')
    mesh_settings.Set('EdgeRefinementOn', '1')
    mesh_settings.Set('EdgeRefinementRatio', '6')
    mesh_settings.SetMeshType('HexTLM')
    mesh_settings.Set('RatioLimitGeometry', '20')
    mesh_settings.SetMeshType('Tet')
    mesh_settings.Set('VolMeshGradation', '1.5')
    mesh_settings.Set('SrfMeshGradation', '1.5')
    mesh_settings.SetMeshType('Hex')
    mesh_settings.Set('Version', '1%')

    meshAdaption3D.SetAdaptionStrategy('Energy')
    mesh.MeshType('PBA')
    PostProcess1D.ActivateOperation('vswr', 'true')
    PostProcess1D.ActivateOperation('yz-matrices', 'true')
    
def units(mws, geometry, frequency, time, temperatureUnit, voltage, current, resistance, conductance, capacitance, inductance):
    units = mws.Units

    units.Geometry(geometry)
    units.Frequency(frequency)
    units.TemperatureUnit(temperatureUnit)
    units.Time(time)
    units.Voltage(voltage)
    units.Current(current)
    units.Resistance(resistance)
    units.Conductance(conductance)
    units.Capacitance(capacitance)
    units.Inductance(inductance)
    
def background_material(mws, xmin, xmax, ymin, ymax, zmin, zmax):
    background = mws.Background
    material = mws.Material

    background.ResetBackground()
    background.Type('Normal')
    background.Epsilon('1.0')
    background.Mu('1.0')
    background.XminSpace(str(xmin))
    background.XmaxSpace(str(xmax))
    background.YminSpace(str(ymin))
    background.YmaxSpace(str(ymax))
    background.ZminSpace(str(zmin))
    background.ZmaxSpace(str(zmax))

    material.Reset()
    material.FrqType('all')
    material.Type('Normal')
    material.MaterialUnit('Frequency', 'Hz')
    material.MaterialUnit('Geometry', 'm')
    material.MaterialUnit('Time', 's')
    material.MaterialUnit('Temperature', 'Kelvin')
    material.Epsilon('1.0')
    material.Mue('1.0')
    material.Sigma('0.0')
    material.TanD('0.0')
    material.TanDFreq('0.0')
    material.TanDGiven('False')
    material.TanDModel('ConstSigma')
    material.EnableUserConstTanDModelOrderEps('False')
    material.ConstTanDModelOrderEps('1')
    material.SetElParametricConductivity('False')
    material.ReferenceCoordSystem('Global')
    material.CoordSystemType('Cartesian')
    material.SigmaM('0')
    material.TanDM('0.0')
    material.TanDMFreq('0.0')
    material.TanDMGiven('False')
    material.TanDMModel('ConstSigma')
    material.EnableUserConstTanDModelOrderMue('False')
    material.ConstTanDModelOrderMue('1')
    material.SetMagParametricConductivity('False')
    material.DispModelEps('None')
    material.DispModelMue('None')
    material.DispersiveFittingSchemeEps('Nth Order')
    material.MaximalOrderNthModelFitEps('10')
    material.ErrorLimitNthModelFitEps('0.1')
    material.UseOnlyDataInSimFreqRangeNthModelEps('False')
    material.DispersiveFittingSchemeMue('Nth Order')
    material.MaximalOrderNthModelFitMue('10')
    material.ErrorLimitNthModelFitMue('0.1')
    material.UseOnlyDataInSimFreqRangeNthModelMue('False')
    material.UseGeneralDispersionEps('False')
    material.UseGeneralDispersionMue('False')
    material.NLAnisotropy('False')
    material.NLAStackingFactor('1')
    material.NLADirectionX('1')
    material.NLADirectionY('0')
    material.NLADirectionZ('0')
    material.Rho('0.0')
    material.ThermalType('Normal')
    material.ThermalConductivity('0.0')
    material.HeatCapacity('0.0')
    material.MetabolicRate('0')
    material.BloodFlow('0')
    material.VoxelConvection('0')
    material.MechanicsType('Unused')
    material.Colour('0.6', '0.6', '0.6')
    material.Wireframe('False')
    material.Reflection('False')
    material.Allowoutline('True')
    material.Transparentoutline('False')
    material.Transparency('0')
    material.ChangeBackgroundMaterial()
    
def mesh_settings(mws, cellsPerWavelength, minCell):
    mesh = mws.Mesh
    mesh_settings = mws.MeshSettings
    discretiser = mws.Discretizer

    mesh.MeshType('PBA')
    mesh.SetCreator('High Frequency')  # warning

    mesh_settings.SetMeshType('Hex')
    mesh_settings.Set('Version', '1%')
    mesh_settings.Set.StepsPerWaveNear(str(cellsPerWavelength))
    mesh_settings.Set.StepsPerWaveFar(str(cellsPerWavelength))
    mesh_settings.Set.WavelengthRefinementSameAsNear('1')
    mesh_settings.Set.StepsPerBoxNear(str(cellsPerWavelength))
    mesh_settings.Set.StepsPerBoxFar(str(cellsPerWavelength))
    mesh_settings.Set.MaxStepNear(str(cellsPerWavelength))
    mesh_settings.Set.MaxStepFar(str(cellsPerWavelength))
    mesh_settings.Set.ModelBoxDescrNear('maxedge')
    mesh_settings.Set.ModelBoxDescrFar('maxedge')
    mesh_settings.Set.UseMaxStepAbsolute('0')
    mesh_settings.Set.GeometryRefinementSameAsNear('1')
    mesh_settings.Set.UseRatioLimitGeometry('1')
    mesh_settings.Set.RatioLimitGeometry(str(minCell))
    mesh_settings.Set.MinStepGeometryX('0')
    mesh_settings.Set.MinStepGeometryY('0')
    mesh_settings.Set.MinStepGeometryZ('0')
    mesh_settings.Set.UseSameMinStepGeometryXYZ('1')
    mesh_settings.SetMeshType('Hex')
    mesh_settings.Set.FaceRefinementOn('0')
    mesh_settings.Set.FaceRefinementPolicy('2')
    mesh_settings.Set.FaceRefinementRatio('2')
    mesh_settings.Set.FaceRefinementStep('0')
    mesh_settings.Set.FaceRefinementNSteps('2')
    mesh_settings.Set.EllipseRefinementOn('0')
    mesh_settings.Set.EllipseRefinementPolicy('2')
    mesh_settings.Set.EllipseRefinementRatio('2')
    mesh_settings.Set.EllipseRefinementStep('0')
    mesh_settings.Set.EllipseRefinementNSteps('2')
    mesh_settings.Set.FaceRefinementBufferLines('3')
    mesh_settings.Set.EdgeRefinementOn('1')
    mesh_settings.Set.EdgeRefinementPolicy('1')
    mesh_settings.Set.EdgeRefinementRatio('2')
    mesh_settings.Set.EdgeRefinementStep('0')
    mesh_settings.Set.EdgeRefinementBufferLines('3')
    mesh_settings.Set.RefineEdgeMaterialGlobal('0')
    mesh_settings.Set.RefineAxialEdgeGlobal('0')
    mesh_settings.Set.BufferLinesNear('3')
    mesh_settings.Set.UseDielectrics('1')
    mesh_settings.Set.EquilibrateOn('0')
    mesh_settings.Set.Equilibrate('1.5')
    mesh_settings.Set.IgnoreThinPanelMaterial('0')
    mesh_settings.SetMeshType('Hex')
    mesh_settings.Set.SnapToAxialEdges('1')
    mesh_settings.Set.SnapToPlanes('1')
    mesh_settings.Set.SnapToSpheres('1')
    mesh_settings.Set.SnapToEllipses('1')
    mesh_settings.Set.SnapToCylinders('1')
    mesh_settings.Set.SnapToCylinderCenters('1')
    mesh_settings.Set.SnapToEllipseCenters('1')

    discretiser.MeshType('PBA')
    discretiser.PBAType('Fast PBA')
    discretiser.AutomaticPBAType('True')
    discretiser.FPBAAccuracyEnhancement('enable')
    discretiser.ConnectivityCheck('False')
    discretiser.ConvertGeometryDataAfterMeshing('True')
    discretiser.UsePecEdgeModel('True')
    discretiser.GapDetection('False')
    discretiser.FPBAGapTolerance('1e-3')
    discretiser.SetMaxParallelMesherThreads('Hex', '12')
    discretiser.SetParallelMesherMode('Hex', 'Maximum')
    discretiser.PointAccEnhancement('0')
    discretiser.UseSplitComponents('True')
    discretiser.EnableSubgridding('False')
    discretiser.PBAFillLimit('99')
    discretiser.AlwaysExcludePec('False')

    

