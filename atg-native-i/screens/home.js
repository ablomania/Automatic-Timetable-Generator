import { useNavigation } from "@react-navigation/native";
import { StyleSheet, View, Text, Button } from "react-native";
import EventList from "../components/events/event-list";
import { useEffect, useState } from "react";
import axios from "axios";

const HomeScreen = () => {
    const [data, setData] = useState([])
    
    useEffect(()=> {
        async function fetchData() {
            try {
                const response = await fetch('http://192.168.1.138:8000/api/schedules/');
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

        fetchData()
    }, [])

    const navigation = useNavigation()
    return(
        <View style={styles.screen}>
            {/* <Text>This is the home screen</Text>
            <Button title="move to detail"
             onPress={() => {navigation.navigate("Details")}}
            /> */}
            <View>
                <EventList data={data}/>
            </View>

        </View>
    );
}

const styles = StyleSheet.create({
    screen: {
        padding: 20,
    }
})

export default HomeScreen;