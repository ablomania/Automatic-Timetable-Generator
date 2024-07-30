import { FlatList, View } from "react-native"
import ScheduleItem from "./schedule-item"
import { useEffect } from "react";
import { apiURL } from "../App";
import AsyncStorage from "@react-native-async-storage/async-storage";

export const ScheduleList = ({data}) => {
    isRefreshing = false
    async function refreshItems() {
        isRefreshing = true;
        const storedDepartmentId = await AsyncStorage.getItem("departmentId");
        const storedTableId = await AsyncStorage.getItem("tableId");
        const storedYearGroup = await AsyncStorage.getItem("yearGroup");
        const response = await fetch(apiURL + storedDepartmentId + '&format=json&table_id=' + storedTableId + '&year_group=' + storedYearGroup);
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
