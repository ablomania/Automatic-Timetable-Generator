import { useNavigation } from "@react-navigation/native";
import { StyleSheet, Text, TouchableOpacity, View } from "react-native";

export const times = {1:"8 am", 2: "9 am", 3: "10 : 30 am", 4: "11 : 30 am", 5: "1 pm", 6: "2 pm", 7:"3 pm", 8:"4 pm", 9:"5 pm", 10:"6 pm", 11:"7 pm", 12:"8 pm", 13:"9 pm", 14:"10 pm"}

export const ScheduleItem = ({item}) => {
    const navigation = useNavigation();

    let time = item.time;
    let day = item.day
    const days = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"};
    return(
        <TouchableOpacity style={styles.container} onPress={() => {navigation.navigate('Details', {item:item, times:times})}}>
            <View style={styles.scheduleItem}>
                <Text style={{fontSize: 30, fontWeight: 'bold'}}>{times[time]}</Text>
                <Text style={{fontSize: 20}}>{item.course_code}</Text>
                <Text style={{fontSize: 15, color: 'grey'}}>{item.location_name}</Text>
                <Text style={{fontSize: 15, color: 'grey'}}>{item.lecturer_name}</Text>
            </View>
        </TouchableOpacity>
   );
}

const styles = StyleSheet.create({
    scheduleItem: {
        padding: 15,
        marginVertical: 10,
        justifyContent: 'center',
        alignItems: 'start',
    },
    container: {
        borderWidth: 1,
        margin: 10,
        borderRadius: 10,
        borderColor: 'grey'
    }
})

export default ScheduleItem;