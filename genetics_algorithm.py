import random


def main(input_file_path, number_of_generation_to_run_for):
    # load customers and ingredient from file
    customers, ingredients = load_customers_and_ingredients(input_file_path)
    genome_size = len(ingredients)
    population_size = genome_size * 5
    n_top_elites = (population_size // 10) + 1

    print(f"Total number of customers: {len(customers)}")

    # randomly create first generation
    current_generation = generate_random_first_population(population_size, genome_size)

    for generation_number in range(number_of_generation_to_run_for):
        print("Generation ", generation_number)
        generation_with_fitness = {}
        next_generation = {}

        # calculate fitness of members
        for member in current_generation:
            member_ingredients = ingredients_genome_to_ingredients(member, ingredients)
            member_fitness = fitness_function(member_ingredients, customers)

            generation_with_fitness[member] = member_fitness

        elites = {member:fitness for member, fitness in sorted(generation_with_fitness.items(), key=lambda item: item[1], reverse=True)[:n_top_elites]}

        for elite in elites:
            next_generation.append(elites)

        while len(next_generation) < population_size:
            child_a, child_b = generate_children(current_generation)
            next_generation.append(child_a)
            next_generation.append(child_b)

        current_generation = next_generation

    most_fit = {member:fitness for member, fitness in sorted(generation_with_fitness.items(), key=lambda item: item[1], reverse=True)[:n_top_elites]}

        print("Elites: ", elites)
        for member,fitness in generation_with_fitness.items():
            print(member, fitness)


def generate_children(parent_generation):
    parent_a, parent_b = select_parents(parent_generat)
    child_a, child_b = cross_over(parent_a, parent_b)
    child_a, child_b = mutate(child_a, child_b)

    return child_a, child_b


def will_order_pizza(ingredient_combination, customer):
    customer_likes, customer_dislikes = customer

    for like in customer_likes:
        if like not in ingredient_combination:
            return False

    for dislike in customer_dislikes:
        if dislike in ingredient_combination:
            return False

    return True


def fitness_function(ingredient_combination, customers):
    customer_count = 0

    for customer in customers:
        if will_order_pizza(ingredient_combination, customer):
            customer_count += 1

    return customer_count


def ingredients_genome_to_ingredients(ingredients_genome, genome_to_ingredient_map):
    ingredients = []
    for idx, genome_bit in enumerate(ingredients_genome):
        if genome_bit:
            ingredients.append(genome_to_ingredient_map[idx])

    return ingredients


def generate_random_first_population(population_size, genome_size):
    generated_population = []

    while len(generated_population) < population_size:
        member = []
        for i in range(genome_size):
            member.append(random.randint(0,1))

        generated_population.append(tuple(member))

    return generated_population


def load_customers_and_ingredients(input_file_path):
    customers = []
    ingredients = []
    with open(input_file_path, 'r') as input_file:
        customer_likes = None
        customer_dislikes = None

        for idx, line in enumerate(input_file):

            if idx == 0:
                total_number_of_customers = int(line)

            elif idx % 2 != 0:
                line_list = line.split()
                if int(line_list[0]) > 0:
                    customer_likes = line_list[1:]
                    ingredients += customer_likes
                else:
                    customer_likes = []
            else:
                line_list = line.split()
                if int(line_list[0]) > 0:
                    customer_dislikes = line_list[1:]
                    ingredients += customer_dislikes
                else:
                    customer_dislikes = []

                customers.append((customer_likes, customer_dislikes))

    ingredients = set(ingredients)
    ingredients = {idx:ingredient for idx,ingredient in enumerate(ingredients)}

    return customers, ingredients



if __name__ == '__main__':
    input_file_path = 'input_data/b_basic.in.txt'
    main(input_file_path, 1)
    # customers, ingredients = load_customers_and_ingredients(input_file_path)
    # print(f"Customers: {len(customers)}\n {customers} \n")
    # print(f"Ingredients: {len(ingredients)}\n {ingredients} \n")

    # print(generate_random_first_population(10, 5))
