import AsyncStorage from "@react-native-async-storage/async-storage";
import { useEffect, useState } from "react";
import { View, FlatList, TouchableOpacity, Text, StyleSheet, SafeAreaView } from 'react-native';
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
        fetchSchedule(department_Id=storedDepartmentId, year_Group=storedYearGroup, table_Id=storedTableId);
    } catch(error){
        console.log("Could not storedData : ", error);
    }
   }
   async function fetchSchedule(department_Id, year_Group, table_Id) {
    try{
        const response = await fetch(apiURL + '/schedules/?department_id=' + department_Id + '&format=json&timetable_id=' + table_Id + '&year_group=' + year_Group);
        if(!response){
            console.log("Bad network response")
        }else{
            const result = await response.json();
            setData(result);
        }
    } catch(error) {
        console.log("Could not fetch schedules : ", error);
    }
   }
   console.log(data)
   return(
    <SafeAreaView style={styles.container}>
        <FlatList 
            data={days} 
            renderItem={({item, index}) => {
            return (
            <View style={styles.listItem}>
                <TouchableOpacity 
                onPress={() =>navigation.navigate('Daily', {data:data, index:index+1})}
                >
                    <Text style={styles.dayText}>
                        {item}
                    </Text>
                </TouchableOpacity>
            </View>
            )
          }} 
          keyExtractor={(item) => item} 
        />
    </SafeAreaView>
   )
}


const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#F5F9FF', // Light blue background
        padding: 16,
    },
    listItem: {
        borderColor: '#007AFF', // Blue border
        borderWidth: 1,
        marginVertical: 5,
        borderRadius: 5,
        marginHorizontal: 2,
        backgroundColor: '#FFFFFF', // White background for each item
    },
    dayText: {
        padding: 30,
        fontSize: 30,
        fontWeight: 'bold',
        color: '#007AFF', // Blue text color
    },
});