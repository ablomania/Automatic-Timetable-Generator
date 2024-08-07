import { View, FlatList } from "react-native";
import ScheduleItem from "../../components/scheduleItem";
import apiURL from '../../App';

export default function Daily({navigation, route }) {
    
    const { data, index } = route.params;
    const dailySchedule = data.filter((dt) => dt.day == index)
    dailySchedule.sort((a, b) => a.time > b.time ? 1 : -1)
    isRefreshing = false
    async function refreshItems() {
        isRefreshing = true;
        const response = await fetch(apiURL + '/schedules/');
        result = response.json();
        data = result;
        isRefreshing = false;
    }
    return(
        <View>
            {/* <Text>This is the home screen</Text>
            <Button title="move to detail"
             onPress={() => {navigation.navigate("Details")}}
            /> */}
            <View>
                <FlatList 
                    data={dailySchedule}
                    renderItem={({item}) => <ScheduleItem item={item} />}
                    keyExtractor={item => item.id}
                    onRefresh={refreshItems}
                    refreshing={isRefreshing}
                />
            </View>

        </View>
    );
}

