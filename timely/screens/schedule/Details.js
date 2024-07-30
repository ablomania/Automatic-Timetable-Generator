import { useLayoutEffect } from "react";
import { Text, View, StyleSheet, TouchableOpacity, ScrollView } from "react-native";


export default function Details({navigation, route}) {
    const {item, times} = route.params;
    console.log(item)
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
        <ScrollView>
            <View style={{padding: 10, justifyContent:'center', marginVertical: 15}}>
                <View style={styles.item}>
                    <Text style={styles.label}>Course Code: </Text>
                    <Text style={styles.value}>{item.course_code}</Text>
                </View>
                <View style={styles.item}>
                    <Text style={styles.label}>Lecturer Name: </Text>
                    <Text style={styles.value}>{item.lecturer_name}</Text>
                </View>
                <View style={styles.item}>
                    <Text style={styles.label}>Location: </Text>
                    <Text style={styles.value}>{item.location_name}</Text>
                </View>
                <View style={styles.item}>
                    <Text style={styles.label}>Time: </Text>
                    <Text style={styles.value}>{times[item.time]}</Text>
                </View>
                <View style={styles.item}>
                    <Text style={styles.label}>Day: </Text>
                    <Text style={styles.value}>{days[item.day]}</Text>
                </View>
                <View style={styles.item}>
                    <Text style={styles.label}>Year Group</Text>
                    <Text style={styles.value}>{item.year_group}</Text>
                </View>
                <TouchableOpacity style={styles.button}>
                    <Text style={{color: '#fff'}}>Add a notification</Text>
                </TouchableOpacity>
                
            </View>
        </ScrollView>
        
    );
}

const styles = StyleSheet.create({
    label: {
        // fontWeight: 'bold',
        fontSize: 20,
        // color: 'grey,'
    },
    item: {
        backgroundColor: '#fafafa',
        marginVertical: 10,
        padding: 10,
        borderRadius: 10
    },
    value: {
        color: '#0d47a1',
        paddingLeft: 30,
    },
    button: {
        backgroundColor: '#1976d2',
        height: 50,
        justifyContent: 'center',
        alignItems: 'center',
        borderRadius: 10,
    }
})