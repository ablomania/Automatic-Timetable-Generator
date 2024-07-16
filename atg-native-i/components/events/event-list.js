import { View, Text, FlatList, RefreshControl } from "react-native"
// import { DUMMY_DATA } from "../../data/dummy_data";
import EventItem from "./event-item";


const EventList = ({data}) => {
    const renderItem = ({schedule}) => {
        return <EventItem 
                    id={schedule.id} 
                    course_code={schedule.course_code}  
                    lecturer_name={schedule.lecturer_name}
                    location_name={schedule.location_name}
                />
    }
    return(
        <View>
            <FlatList 
                data={data}
                keyExtractor={schedule => schedule.id} 
                renderItem={renderItem}
                refreshControl={
                    <RefreshControl
                        refreshing={false}
                        onRefresh={() => console.log('refreshing ... ...')}
                    />
                }
                // numColumns={2}
                />
        </View>
    )
}

export default EventList;