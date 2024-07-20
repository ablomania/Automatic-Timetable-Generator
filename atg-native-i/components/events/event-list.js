import { View, Text, FlatList, RefreshControl } from "react-native"
// import { DUMMY_DATA } from "../../data/dummy_data";
import EventItem from "./event-item";


const EventList = ({data}) => {
    const renderItem = () => {
        return <EventItem 
                    id={data.id} 
                    course_code={data.course_code}  
                    lecturer_name={data.lecturer_name}
                    location_name={data.location_name}
                />
    }
    return(
        <View>
            <FlatList 
                data={data}
                keyExtractor={data => data.id} 
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