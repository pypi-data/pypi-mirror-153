# mmWave Package

[![Version](https://img.shields.io/pypi/v/ipyvolume.svg)](https://pypi.org/project/mmWave/)

This is a mmWave data parsing library package work with Joybien mmWave EVM Kit.

## libray include:
1. vitalsign v0.0.10
2.  highAccuraccy v0.0.4
3. peopleMB v0.0.4
4. srradar v0.0.1
5. people3D v0.0.2
6. pc3d v0.0.3
7. pc3d_kv v0.0.2
8. lpdISK v0.0.1
9. lpdISK_kv v0.0.1
10. vehicleOD v0.0.1   (deprecated)
11. trafficMD_kv v0.0.2
12. surfaceVD v0.0.1
13. trafficMD v0.1.0    update:2021/04/21
14. droneRN v0.0.2
15. pc3 v0.1.4          update:2021/10/12(doppler & range swap: seq:eadrs)
16. vehicleODHeatMap v0.0.1
17. vitalsign_kv v0.0.1
18. vehicleODR v0.0.1  (VOD: Vehicle Occupancy Detection)
19. roadwayTMD_kv v0.1.2 update:2021/05/04 (TRS: Traffic monitoring detection Roadway Sensing )
20. pc3OVH v0.1.2    2021/08/12(OVH: OVerHead) 
21. lpdFDS  v0.1.2    updated:2021/05/26 (FDS: Falling Detection Sensing) 
22. trafficMD_I480 v0.1.0   2021/09/16 (Traffic Monitoring Detection version:I480)
            v0.1.1 2022/03/10 bug fix
            v2.0.1 2022/04/28 (output data posZ,velZ,accZ position change)
23. mrRadar v0.0.1 2021/12/31 released (MRR: Medium Range Radar)
            v0.0.2 2022/02/07 format revised
            v0.1.0 2022/06/02 fit v3 data
24. pc3_oob v0.0.1 2022/03/01 first released
            v0.0.2 2022/03/01 bug fix
            v0.0.3 2022/03/03
25. pc3_vsd v0.0.1 2022/03/10 Bata version
26. pc3_v2  v2     2022/04/19 first released
27. trafficMD_I480 v2.0.1 2022/04/28 (output data posZ,velZ,accZ position change)
                   v2.0.2/3 added tlvRead status, chk: {0:'EMPTY',1:'inData',10:'IDLE',99:'FALSE'}
                   v2.0.4 added tlvRead status, chk: {0:'EMPTY',1:'inData',10:'IDLE',99:'FALSE'}

## Example code 
- Example code you can down load from [GitHub](https://github.com/bigheadG/mmWave) if you found any bugs or have any suggestions Please submit issues to Github

## installation
```
pip3 install mmWave
```

## update history
1. 2021/09/16 pc3OVH v0.1.2 : @v7 dataFrame colume change. 'tid' move to front of 'ec0'
2. 2021/10/12 pc3    v0.1.4   update:(doppler & range swap: seq:eadrs)
3. mmWave-0.1.62
   2021/12/31 MRR    v0.0.1   added MRR
4. mmWave-0.1.63
   2022/02/07 MRR    v0.0.2   update(format revised)
5. mmWave-0.1.64
   2022/03/01 pc3_oob v0.0.1  added pc3_oob
5. mmWave-0.1.65
   2022/03/01 pc3_oob v0.0.2  bug fix
   2022/03/03 pc3_oob v0.0.3  bug fix
6. mmWave-1.0.68   
   2022/03/10 pc3_vsd v0.0.1  beta version 
   
7. mmWave-1.0.70   
   2022/04/19 pc3_v2 v2.0 @copy from pc3OVH

8. mmWave-1.0.71   
   2022/04/28 trafficMD_I480 v2.0.1 (output data posZ,velZ,accZ position change)
9. mmWave-1.0.72 (remove)
10. mmWave-1.0.73  
   2022/05/12 trafficMD_I480 v2.0.2 "added tlvRead status, chk: {0:'EMPTY',1:'inData',10:'IDLE',99:'FALSE'}
11. mmWave-1.0.74  
    2022/05/15 trafficMD_I480 v2.0.4 revised v8,v9 as dictionay data type

12. mmWave-1.0.75  
    2022/06/02 mrRadar revised to fit v3 
