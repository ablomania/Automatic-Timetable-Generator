import { createDrawerNavigator, DrawerItem, DrawerItemList } from '@react-navigation/drawer';
// import HomeScreen from '../screens/home';
import { HomeStack, ProfileStack } from './stack';
import { View, Image, Linking } from 'react-native';
import { Ionicons, MaterialCommunityIcons } from '@expo/vector-icons';

const Drawer = createDrawerNavigator();

export default function MyDrawer() {
  return (
    <Drawer.Navigator
        drawerContent={(props) => {
            return (
                <View style={{flex:1, paddingTop:20, }}>
                    <View style={{height: 140, justifyContent: 'center', alignItems: 'center'}}>
                        <Image
                            style={{width:100, resizeMode: 'contain'}}
                            source={require("../assets/images/fixit.png")}
                        />
                    </View>
                    <DrawerItemList {...props} />
                    <DrawerItem 
                        label="More Info"
                        onPress={()=> Linking.openURL('https://google.com')}
                        icon={() => (
                            <Ionicons name="information" size={22}/>
                        )}
                    />

                </View>
            );
        }}
        screenOptions={{headerShown:false}}>
      <Drawer.Screen name="HomeStack" component={HomeStack} options={
        {
            title: 'Home',
            drawerIcon: () => <Ionicons name="home" size={22} />
        }
      }/>
      <Drawer.Screen name="ProfileStack" component={ProfileStack} options={
        {
            title: 'Profiles',
            drawerIcon: () => <MaterialCommunityIcons name='face-man-profile' size={22} />
        }
      }/>
    </Drawer.Navigator>
  );
}