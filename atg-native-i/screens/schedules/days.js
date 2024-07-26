import { useNavigation } from "@react-navigation/native";
import { useEffect, useState } from "react";
import { StyleSheet, View, Text, TouchableOpacity, FlatList } from "react-native";
import DaysList from "../../components/days-list";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { apiURL } from "../../App";


export default function ScheduleDaysScreen({navigation}) {

    const [data, setData] = useState([])

    const getStoredData = async () => {
        try {
          const storedTableId = await AsyncStorage.getItem('tableId');
          const storedCollegeId = await AsyncStorage.getItem('collegeId');
          const storedYearGroup = await AsyncStorage.getItem('yearGroup');
          const storedDepartmentId = await AsyncStorage.getItem('departmentId');
          console.log(storedDepartmentId)
          fetchSchedules(tableId=storedTableId, departmentId=storedDepartmentId, yearGroup=storedYearGroup)
        } catch (error) {
          console.error('Error retrieving data:', error);
        }
    }
    async function fetchSchedules(tableId, departmentId, yearGroup) {
        try {
            const response = await fetch(apiURL + '/schedules/?department_id=' + departmentId + '&format=json&table_id=' + tableId + '&year_group=' + yearGroup);
            if(!response.ok) {
                throw new Error('Network response was not ok');
            }
            const result  = await response.json();
            console.log(result);
            setData(result);
        }
        catch(error) {
            console.error('Error fetching data: ', error);
        }
    }

    useEffect(()=> {
        getStoredData();
    }, [])

    return (
        <View>
            <DaysList data={data} />
        </View>
    );
}