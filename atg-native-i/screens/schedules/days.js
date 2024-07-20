import { useNavigation } from "@react-navigation/native";
import { useEffect, useState } from "react";
import { StyleSheet, View, Text, TouchableOpacity, FlatList } from "react-native";
import DaysList from "../../components/days-list";
import AsyncStorage from "@react-native-async-storage/async-storage";


export default function ScheduleDaysScreen() {
    const navigation = useNavigation();

    const [data, setData] = useState([])
    
    useEffect(()=> {
        async function fetchData() {
            try {
                const response = await fetch('http://192.168.1.193:8000/api/schedules/');
                if(!response.ok) {
                    throw new Error('Network response was not ok');
                }
                const result  = await response.json();
                
                setData(result);
            }
            catch(error) {
                console.error('Error fetching data: ', error);
            }
        }

        fetchData()
    }, [])

    return (
        <View>
            <DaysList data={data} />
        </View>
    );
}