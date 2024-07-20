import { SafeAreaView, Text, View } from "react-native";

export default function HomeScreen({navigation}) {
    const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

    const date = new Date();
    let today = date.getDay() - 1;
    
    return(
        <SafeAreaView>
        <View>
            <Text style={{fontWeight:'bold', fontSize:20}}>{days[today]}</Text>
        </View>
        </SafeAreaView>
        
    )
}