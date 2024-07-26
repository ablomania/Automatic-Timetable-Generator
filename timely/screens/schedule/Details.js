import { useLayoutEffect } from "react";
import { Text, View, StyleSheet } from "react-native";


export default function Details({navigation, route}) {
    const {item, times} = route.params;
    const days = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"};
    // useLayoutEffect(() => {
    //     navigation.setOptions({
    //         headerTitle: "new title",
    //         headerLeft:() => (
    //             <HeaderBackButton 
    //             // tintColor = "white"
    //             onPress = {() => navigation.goBack()}
    //             />
    //         )
    //     },[])
    // })
    return(
        <View style={{padding: 10, justifyContent:'center'}}>
            <Text style={{padding: 5}}>Course Code: </Text>
            <Text>{item.course_code}</Text>
            <Text style={{padding: 5}}>Lecturer Name: </Text>
            <Text>{item.lecturer_name}</Text>
            <Text style={{padding: 5}}>Location: </Text>
            <Text>{item.location_name}</Text>
            <Text style={{padding: 5}}>Time: </Text>
            <Text>{times[item.time]}</Text>
            <Text>Day: </Text>
            <Text>{days[item.day]}</Text>
            <Text>Year Group</Text>
            <Text>{item.year_group}</Text>
        </View>
    );
}