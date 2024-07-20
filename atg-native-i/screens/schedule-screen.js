import { useNavigation } from "@react-navigation/native";
import { StyleSheet, View, Text, Button } from "react-native";
import EventList from "../components/events/event-list";
import { useEffect, useState } from "react";
import axios from "axios";
import ScheduleList from "../components/schedule-list";

const ScheduleScreen = ({route, navigation}) => {
    const { data, index } = route.params;

    const dailySchedule = data.filter((dt) => dt.day == index)
    return(
        <View style={styles.screen}>
            {/* <Text>This is the home screen</Text>
            <Button title="move to detail"
             onPress={() => {navigation.navigate("Details")}}
            /> */}
            <View>
                <ScheduleList data={dailySchedule}/>
            </View>

        </View>
    );
}

const styles = StyleSheet.create({
    screen: {
        padding: 20,
    }
})

export default ScheduleScreen;