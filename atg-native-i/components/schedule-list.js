import { FlatList, View } from "react-native"
import ScheduleItem from "./schedule-item"
import { useEffect } from "react";
import { apiURL } from "../App";

const ScheduleList = ({data}) => {
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