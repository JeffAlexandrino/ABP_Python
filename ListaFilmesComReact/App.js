import React, { useState, useEffect } from 'react';
import { View, Text, Button, FlatList, TouchableOpacity, StyleSheet } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';


function HomeScreen({ navigation }) {
  const [movies, setMovies] = useState([]);

  
  useEffect(() => {
    fetch('https://reactnative.dev/movies.json') 
      .then(response => response.json())
      .then(data => setMovies(data.movies)) 
      .catch(error => console.error(error));
  }, []);

  
  const renderMovieItem = ({ item }) => (
    <TouchableOpacity onPress={() => navigation.navigate('Details', { movie: item })}>
      <Text style={styles.movieTitle}>{item.title}</Text>
    </TouchableOpacity>
  );

  return (
    <View style={styles.container}>
      <Text style={styles.header}>Lista de Filmes</Text>
      <FlatList
        data={movies} 
        keyExtractor={(item) => item.id.toString()}
        renderItem={renderMovieItem} 
      />
    </View>
  );
}


function DetailsScreen({ route, navigation }) {
  const { movie } = route.params; 

  return (
    <View style={{ flex: 1, alignItems: 'center', justifyContent: 'center' }}>
      <Text style={styles.title}>Detalhes do Filme</Text>
      <Text style={styles.movieDetail}>Título: {movie.title}</Text>
      <Text style={styles.movieDetail}>Ano de Lançamento: {movie.releaseYear}</Text>
      <Button title="Voltar para home" onPress={() => navigation.goBack()} />
    </View>
  );
}


const Stack = createNativeStackNavigator();

export default function App() {
  return (
    <NavigationContainer>
      <Stack.Navigator initialRouteName="Home">
        <Stack.Screen name="Home" component={HomeScreen} options={{ title: 'Lista de Filmes' }} />
        <Stack.Screen name="Details" component={DetailsScreen} options={{ title: 'Detalhes do Filme' }} />
      </Stack.Navigator>
    </NavigationContainer>
  );
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 20,
  },
  header: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 20,
    textAlign: 'center',
  },
  movieTitle: {
    fontSize: 18,
    paddingVertical: 10,
    borderBottomWidth: 1,
    borderBottomColor: '#ccc',
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 10,
  },
  movieDetail: {
    fontSize: 18,
    marginBottom: 10,
  },
});
