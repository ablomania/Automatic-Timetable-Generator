import { useNavigation } from "@react-navigation/native";
import { Touchable, TouchableOpacity, Text, StyleSheet } from "react-native"

const EventItem = ({id, course_code, lecturer_name, location_name}) => {
    const navigation = useNavigation()
    return(
        <TouchableOpacity style={styles.card} onPress={()=> navigation.navigate("Details", {eventId: id, course_code, lecturer_name, location_name})}>
            <Text>{course_code}</Text>
            <Text>{location_name}</Text>
            <Text>{lecturer_name}</Text>
        </TouchableOpacity>
    );
}

const styles = StyleSheet.create({
    card: {
        borderWidth: 1,
        borderColor: '#c5c5c5',
        borderRadius: 10,
        marginVertical:5,
        padding:30,
    }
})

export default EventItem;