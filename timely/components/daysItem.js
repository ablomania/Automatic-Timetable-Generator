import { Text, TouchableOpacity, View } from "react-native"

export default function DaysItem({day}) {
    const days = {1: "Monday", 2: "Tuesday", 3: "Wednesday", 4: "Thursday", 5: "Friday", 6: "Saturday", 7: "Sunday"};
    return(
        <View>
            <TouchableOpacity>
                <Text>{day}</Text>
            </TouchableOpacity>
            
        </View>
    )
}