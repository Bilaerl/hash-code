import random


def main(number_of_generation_to_run_for, input_file_path, output_file_path=None):
    # load customers and ingredient from file
    customers, ingredients = load_customers_and_ingredients(input_file_path)
    genome_size = len(ingredients)
    population_size = genome_size * 5

    # make population size even so there won't be
    # overflow when adding children
    if population_size % 2 != 0:
        population_size += 1

    population_size = population_size if population_size < 250 else 250

    print(population_size, genome_size)
    naive_vect = [0 for i in ingredients.keys()]
    naive_ingr = suggest_ingredients(input_file_path)

    for ind, ingr in ingredients.items():
        if ingr in naive_ingr:
            naive_vect[ind] = 1
    naive_vect = tuple(naive_vect)
    # make n_top_elites even so there won't be
    # overflow when adding children
    n_top_elites = 2 if population_size < 10 else 10
    # if (n_top_elites % 2 != 0) and (n_top_elites+1 < population_size):
    #     n_top_elites += 1


    print(f"Total number of customers: {len(customers)}")

    # randomly create first generation
    current_generation = generate_random_first_population(population_size, genome_size, naive_vect)

    for generation_number in range(number_of_generation_to_run_for):
        print("Generation ", generation_number)
        current_generation_with_fitness = {}
        next_generation = []

        # calculate fitness of members
        for member in current_generation:
            if member not in current_generation_with_fitness:
                member_ingredients = ingredients_genome_to_ingredients(member, ingredients)
                member_fitness = fitness_function(member_ingredients, customers)

                current_generation_with_fitness[member] = member_fitness

        elites = {member:fitness for member, fitness in sorted(current_generation_with_fitness.items(), key=lambda item: item[1], reverse=True)[:n_top_elites]}

        for elite in elites:
            next_generation.append(elite)

        while len(next_generation) < population_size:
            child_a, child_b = generate_children(current_generation_with_fitness)
            next_generation.append(child_a)
            next_generation.append(child_b)

        print("Elites: ", list(elites.values()))
        print("Population size: ", len(current_generation))
        for member in current_generation:
            print(current_generation_with_fitness[member], end="\t")

        print()

        current_generation = next_generation

    most_fit, most_fit_val = select_most_fit(current_generation, ingredients, customers)

    print(f"Most fit: ", most_fit, most_fit_val)
    with open(output_file_path, 'w') as out_file:
        output = f"{len(most_fit)}"
        for ingredient in most_fit:
            output += f" {ingredient}"

        out_file.write(output)


def select_most_fit(population, ingredients, customers):
    most_fit = None
    most_fit_val = 0

    for member in population:
        member_ingredients = ingredients_genome_to_ingredients(member, ingredients)
        member_fitness = fitness_function(member_ingredients, customers)

        if member_fitness > most_fit_val:
            most_fit = member_ingredients
            most_fit_val = member_fitness

    return most_fit, most_fit_val


def generate_children(parent_generation):
    parent_a, parent_b = select_parents(parent_generation)
    child_a, child_b = cross_over(parent_a, parent_b)
    child_a = mutate(child_a)
    child_b = mutate(child_b)

    return child_a, child_b


def select_parents(parent_generation):
    parents = list(parent_generation.keys())
    selected_parents = []

    for i in range(2):
        candidate_a, candidate_b = random.sample(parents, 2)

        if parent_generation[candidate_a] > parent_generation[candidate_b]:
            selected_parents.append(candidate_a)
        else:
            selected_parents.append(candidate_b)

    return selected_parents


def cross_over(parent_a, parent_b):
    genome_length = len(parent_a)
    half = genome_length//2

    child_a = parent_a[:half] + parent_b[half:]
    child_b = parent_b[:half] + parent_a[half:]

    return child_a, child_b


def mutate(genome):
    mutated_genome = list(genome)
    for idx, genome_bit in enumerate(genome):
        num = random.random()
        if num < 0.005:
            mutated_genome[idx] = int(not bool(mutated_genome[idx]))

    return tuple(mutated_genome)


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


def generate_random_first_population(population_size, genome_size, naive):
    generated_population = [naive]

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


from collections import Counter


def find_ingredients(likes, dislikes):
    ingredient = []
    for ing in likes.keys():
        if ing not in dislikes:
            ingredient.append(ing)
        else:
            if likes[ing] >= dislikes[ing]:
                ingredient.append(ing)
    num_ingr = len(ingredient)
    # ingredient.insert(0, str(num_ingr))
    return ingredient


def calc_costumers(customers, ingredients):
    num_cus = 0

    for customer in customers:
        if all([elem in ingredients for elem in customer[0]]) and not any(
                [elem in ingredients for elem in customer[1]]):
            num_cus += 1
    return num_cus


def suggest_ingredients(FILE):

    with open(FILE) as file:
        lines = file.readlines()
        lines = [line.replace('\n', '') for line in lines]
        file.close()

    num_cus = int(lines.pop(0))
    n = 0
    indxs = []
    customers = []
    likes, dislikes = [],[]

    for i in range(num_cus):
        indxs.append(n)
        n += 2
    for indx in indxs:
        like = lines[indx].split()[1:]
        dislike = [] if lines[indx+1] == '0' else lines[indx+1].split()[1:]
        customers.append([like, dislike])
        likes += like
        dislikes += dislike

    likes, dislikes = Counter(likes), Counter(dislikes)
    ingredients = find_ingredients(likes, dislikes)
    return ingredients
    # with open(FILE.replace('in', 'out'), 'w') as out_file:
    #     out_file.write(ingredients)
    #     out_file.close()


if __name__ == '__main__':
    input_file_path = 'input_data/e_elaborate.in.txt'
    output_file_path = 'output/' + input_file_path.split('/')[1]
    # print(output_file_path)
    main(100, input_file_path, output_file_path)
    # customers, ingredients = load_customers_and_ingredients(input_file_path)
    # print(f"Customers: {len(customers)}\n {customers} \n")
    # print(f"Ingredients: {len(ingredients)}\n {ingredients} \n")

    # print(generate_random_first_population(10, 5))


