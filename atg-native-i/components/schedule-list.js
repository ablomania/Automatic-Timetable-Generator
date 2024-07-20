import { FlatList, View } from "react-native"
import ScheduleItem from "./schedule-item"
import { useEffect } from "react";

const ScheduleList = ({data}) => {
    isRefreshing = false
    async function refreshItems() {
        isRefreshing = true;
        const response = await fetch('http://192.168.1.193:8000/api/schedules/');
        result = response.json();
        data = result;
        isRefreshing = false;
    }
    
    return(
        <View>
            <FlatList 
                data={data}
                renderItem={({item}) => <ScheduleItem item={item} />}
                keyExtractor={item => item.id}
                onRefresh={refreshItems}
                refreshing={isRefreshing}
            />
        </View>
    )
    
}

export default ScheduleList;