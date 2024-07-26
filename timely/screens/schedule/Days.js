import AsyncStorage from "@react-native-async-storage/async-storage";
import { useEffect, useState } from "react";
import { View, FlatList, TouchableOpacity, Text } from 'react-native';
import { apiURL } from "../../App";


export default function Days({navigation}) {
   const [ data, setData] = useState([]);
   const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"];

   useEffect(() => {
    getStoredData();
   },[])

   async function getStoredData() {
    try{
        const storedDepartmentId = await AsyncStorage.getItem("departmentId");
        const storedYearGroup = await AsyncStorage.getItem("yearGroup");
        const storedTableId = await AsyncStorage.getItem("tableId");
        console.log(storedDepartmentId)
        fetchSchedule(department_Id=storedDepartmentId, year_Group=storedYearGroup, table_Id=storedTableId);
    } catch(error){
        console.log("Could not storedData : ", error);
    }
   }
   async function fetchSchedule(department_Id, year_Group, table_Id) {
    try{
        const response = await fetch(apiURL + '/schedules/?department_id=' + department_Id + '&format=json&table_id=' + table_Id + '&year_group=' + year_Group);
        if(!response){
            console.log("Bad network response")
        }else{
            console.log("dfdf")
            const result = await response.json();
            console.log("rr", result)
            setData(result);
        }
    } catch(error) {
        console.log("Could not fetch schedules : ", error);
    }
   }

   return(
    <View>
        <FlatList 
            data={days} 
            renderItem={({item, index}) => {
            return (
            <View style={{borderColor: 'black', borderWidth: 1, marginVertical: 5, borderRadius:5, marginHorizontal: 2}}>
                <TouchableOpacity 
                onPress={() =>navigation.navigate('Daily', {data:data, index:index+1})}
                >
                    <Text style={{padding: 30, fontSize: 30, fontWeight: 'bold'}}>
                        {item}
                    </Text>
                </TouchableOpacity>
            </View>
            )
          }} 
          keyExtractor={(item) => item} 
        />
    </View>
   )
}