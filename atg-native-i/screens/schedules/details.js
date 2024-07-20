import { useRoute, useNavigation } from "@react-navigation/native";
import { useLayoutEffect } from "react";
import { StyleSheet, View, Text } from "react-native";
import { HeaderBackButton } from "@react-navigation/elements";


const DetailScreen = ({route, navigation}) => {

    const {item, times} = route.params;
    const days = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"}

    useLayoutEffect(() => {
        navigation.setOptions({
            headerTitle: "new title",
            headerLeft:() => (
                <HeaderBackButton 
                // tintColor = "white"
                onPress = {() => navigation.goBack()}
                />
            )
        },[])
    })
    return(
        <View style={styles.screen}>
                <Text style={{padding: 5}}>Course Code: {item.course_code}</Text>
                <Text style={{padding: 5}}>Lecturer Name: {item.lecturer_name}</Text>
                <Text style={{padding: 5}}>Location: {item.location_name}</Text>
                <Text style={{padding: 5}}>Time: {times[item.time]}</Text>
                <Text>Day: {days[item.day]}</Text>
                <Text>{item.year_group}</Text>
            <Text>KK</Text>
        </View>
    );
}

const styles = StyleSheet.create({
    screen: {
        padding: 20,
    }
})

export default DetailScreen;