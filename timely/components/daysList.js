import { FlatList, ScrollView, Text, TouchableOpacity, View } from "react-native"
import { useNavigation } from "@react-navigation/native";

export default function DaysList({data}) {
    const days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];

    const navigation = useNavigation()
    return (
        <FlatList 
            data={days} 
            renderItem={({item, index}) => {
            return (
            <View style={{borderColor: 'black', borderWidth: 1, marginVertical: 5, borderRadius:5, marginHorizontal: 2}}>
                <TouchableOpacity onPress={() =>navigation.navigate('Daily', {data:data, index:index+1})}>
                    <Text style={{padding: 30, fontSize: 30, fontWeight: 'bold'}}>
                        {item}
                    </Text>
                </TouchableOpacity>
            </View>
            )
          }} 
          keyExtractor={(item) => item} 
        />
    )
}