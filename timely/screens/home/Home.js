import { FlatList, SafeAreaView, StyleSheet, Text, TouchableOpacity, View } from "react-native";
import { useEffect, useState } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { apiURL } from "../../App";
import { useNavigation } from "@react-navigation/native";
import Constants from "expo-constants"

export default function Home() {
    const times = {1:"8 am", 2: "9 am", 3: "10 : 30 am", 4: "11 : 30 am", 5: "1 pm", 6: "2 pm", 7:"3 pm", 8:"4 pm", 9:"5 pm", 10:"6 pm", 11:"7 pm", 12:"8 pm", 13:"9 pm", 14:"10 pm"}
    const days = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

    const navigation = useNavigation();

    const date = new Date();
    const currentTime = date.getHours();
    const day = date.getDate();
    const month = date.getMonth() + 1;
    const year = date.getFullYear();
    const today = date.getDay();
    console.log("td",today)
    const [ todaySchedule, setTodaySchedule ] = useState([]);
    const [ currentItem, setCurrentItem ] = useState([]);
    const [ firstElement, setFirstElement ] = useState([]);
    const [ isRefreshing, setIsrefreshing ] = useState(false);

    useEffect(() => {
        getStoredData()
    }, [])
    async function fetchData(departmentId, yearGroup, tableId) {
        try{
            setIsrefreshing(true);
            const response = await fetch(apiURL + '/schedules/?department_id=' + departmentId + '&format=json&timetable_id=' + tableId + '&year_group=' + yearGroup)
            if(!response) {
                console.log("Bad network");
            } else {
                const result = await response.json();
                const data = result;
                const dte = data.filter((dt)=> dt.day == today);
                let sortedData = dte.sort((a,b) => a.time > b.time ? 1: -1);
                let filteredData = sortedData.filter((sd) => sd.time + 7 > currentTime);
                setFirstElement(filteredData.splice(0,1));
                setTodaySchedule(filteredData);
                setIsrefreshing(false);
            }
        } catch(error) {
            console.log("Error fetching data for home : ", error);
        }finally{
            
        }
    }
    async function getStoredData() {
        const storedDepartmentId = await AsyncStorage.getItem("departmentId")
        const storedYearGroup = await AsyncStorage.getItem("yearGroup");
        const storedTableId = await AsyncStorage.getItem("tableId");
        await fetchData(departmentId=storedDepartmentId, yearGroup=storedYearGroup, tableId=storedTableId);
    }
    return(
        <SafeAreaView style={styles.container}>
            <View>
                <Text style={styles.dayText}>{days[today]}</Text>
                <Text style={styles.dateText}>{day} - {month} - {year}</Text>
                <Text style={styles.upcomingClassText}>Upcoming Class</Text>
                {firstElement.length ? (
                    <TouchableOpacity onPress={() => navigation.navigate('Details', { item: firstElement[0], times })}>
                        <Text style={styles.upcomingClassInfo}>{times[firstElement[0].time]}</Text>
                        <Text style={styles.classDetails}>{firstElement[0].course_code}</Text>
                        <Text style={styles.classDetails}>{firstElement[0].location_name}</Text>
                        <Text style={styles.classDetails}>{firstElement[0].lecturer_name}</Text>
                    </TouchableOpacity>
                ) : (
                    <Text style={styles.noClassesText}>No upcoming classes</Text>
                )}
            </View>
            {todaySchedule.length>1  ? (
                <FlatList
                    data={todaySchedule}
                    keyExtractor={(sch) => sch.id}
                    onRefresh={() => getStoredData()} // Implement your refresh logic
                    refreshing={isRefreshing}
                    renderItem={({ sch }) => (
                        <View style={styles.scheduleItem}>
                            <TouchableOpacity onPress={() => navigation.navigate('Schedules',  {screen: "Details", item: sch, times })}>
                                <Text style={styles.upcomingClassInfo}>{times[sch.time]}</Text>
                                <Text style={styles.classDetails}>{sch.location_name}</Text>
                                <Text style={styles.lecturerText}>{sch.lecturer_name}</Text>
                            </TouchableOpacity>
                        </View>
                    )}
                />
                 ) : (
                        <View style={styles.scheduleItem}>
                            <Text>Nothing More</Text>
                        </View>
            )}
            
        </SafeAreaView>
        

    )
}


const styles = StyleSheet.create({
    container: {
        flex: 1,
        backgroundColor: '#fff',
        padding: 16,
    },
    dayText: {
        color: '#333',
        fontSize: 18,
        marginBottom: 8,
    },
    dateText: {
        color: '#666',
        fontSize: 14,
        marginBottom: 16,
    },
    upcomingClassText: {
        fontSize: 20,
        fontWeight: 'bold',
        marginBottom: 16,
    },
    upcomingClassInfo: {
        fontSize: 16,
        color: '#007AFF',
        marginBottom: 8,
    },
    classDetails: {
        fontSize: 14,
        color: '#444',
        marginBottom: 4,
    },
    noClassesText: {
        fontWeight: 'bold',
        color: '#888',
    },
    scheduleItem: {
        marginVertical: 10,
        padding: 16,
        borderBottomWidth: 1,
        borderColor: '#ddd',
    },
    lecturerText: {
        fontSize: 12,
        color: '#888',
    },
});
